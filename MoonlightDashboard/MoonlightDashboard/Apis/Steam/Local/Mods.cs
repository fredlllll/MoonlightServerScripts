using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using System.Text.Json;

namespace MoonlightDashboard.Apis.Steam.Local
{
    public static class Mods
    {
        private static HttpClient _httpClient = new HttpClient();

        public static string GetWorkshopModsFolder()
        {
            return Path.Combine(Steam.GetSteamFolderPath(), "steamapps", "workshop", "content", Constants.ARMA3APPID);
        }

        public static string GetModFolder(string modId)
        {
            return Path.Combine(GetWorkshopModsFolder(), modId);
        }

        public static async Task<string> GetModName(string modId)
        {
            try
            {
                var formData = new Dictionary<string, string>
                {
                    { "itemcount", "1" },
                    { "publishedfileids[0]", modId }
                };

                // Create content with application/x-www-form-urlencoded media type
                using var content = new FormUrlEncodedContent(formData);

                var response = await _httpClient.PostAsync(
                    "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
                    content
                );

                if (response.StatusCode != System.Net.HttpStatusCode.OK)
                {
                    return modId;
                }

                var responseString = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(responseString);
                var root = jsonDoc.RootElement;

                // Navigate JSON: response -> publishedfiledetails -> [0] -> title
                if (root.TryGetProperty("response", out var responseProp) &&
                    responseProp.TryGetProperty("publishedfiledetails", out var detailsProp) &&
                    detailsProp.GetArrayLength() > 0 &&
                    detailsProp[0].TryGetProperty("title", out var titleProp))
                {
                    return titleProp.GetString() ?? throw new Exception($"title in response is null. Raw: {responseString}");
                }
                else
                {
                    // Match Python KeyError catch: log warning (console here) and return ID
                    Console.WriteLine($"Warning: Unexpected JSON structure for mod {modId}. Raw: {responseString}");
                    return modId;
                }
            }
            catch (Exception ex)
            {
                // Handle network errors or JSON parsing errors
                Console.WriteLine($"Error fetching mod name for {modId}: {ex.Message}");
                return modId;
            }
        }

        public static IEnumerable<string> GetDownloadedModsIds()
        {
            var workshopModsFolder = new DirectoryInfo(GetWorkshopModsFolder());
            if (workshopModsFolder.Exists)
            {
                foreach (var dir in workshopModsFolder.EnumerateDirectories())
                {
                    yield return dir.Name;
                }
            }
        }

        public static async Task<IEnumerable<ModInfo>> GetModInfos(DatabaseContext db, IEnumerable<string> modIds)
        {
            var threshold = DateTime.UtcNow.AddDays(-7);

            var infos = db.ModInfos.Where(m => modIds.Contains(m.ModId)).ToList();

            var existingIds = new HashSet<string>(infos.Select(m => m.ModId));

            var missingIds = modIds.Where(id => !existingIds.Contains(id)).ToList();

            var outdatedInfos = infos.Where(m => m.Updated < threshold).ToList();
            foreach (var info in outdatedInfos)
            {
                info.Name = await GetModName(info.ModId);
                info.Updated = DateTime.UtcNow;
            }
            foreach (var id in missingIds)
            {
                var mi = new ModInfo()
                {
                    Id = Util.GetNewId<ModInfo>(),
                    ModId = id,
                    Name = await GetModName(id)
                };
                infos.Add(mi);
                db.ModInfos.Add(mi);
            }
            db.SaveChanges();
            return infos;
        }

        public static void DeleteMod(string modId)
        {
            var folder = GetModFolder(modId);
            if (Directory.Exists(folder))
            {
                Directory.Delete(folder, true);
            }
        }

        public static async Task<List<string>> GetCollectionModIds(string collectionId)
        {
            List<string> result = new List<string>();
            try
            {
                var formData = new Dictionary<string, string>
                {
                    { "collectioncount", "1" },
                    { "publishedfileids[0]", collectionId }
                };

                // Create content with application/x-www-form-urlencoded media type
                using var content = new FormUrlEncodedContent(formData);

                var response = await _httpClient.PostAsync(
                    "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/",
                    content
                );

                if (response.StatusCode != System.Net.HttpStatusCode.OK)
                {
                    return result;
                }

                var responseString = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(responseString);
                var root = jsonDoc.RootElement;

                // Navigate JSON: response -> publishedfiledetails -> [0] -> title
                if (root.TryGetProperty("response", out var responseProp) &&
                    responseProp.TryGetProperty("collectiondetail", out var detailsProp) &&
                    detailsProp.GetArrayLength() > 0 &&
                    detailsProp[0].TryGetProperty("children", out var childrenProp) &&
                    childrenProp.GetArrayLength() > 0)
                {
                    foreach (var element in childrenProp.EnumerateArray())
                    {
                        result.Add(element.GetProperty("publishedfileid").ToString());
                    }
                    return result;
                }
                else
                {
                    Console.WriteLine($"Warning: Unexpected JSON structure for collection {collectionId}. Raw: {responseString}");
                    return result;
                }
            }
            catch (Exception ex)
            {
                // Handle network errors or JSON parsing errors
                Console.WriteLine($"Error fetching mods for collection {collectionId}: {ex.Message}");
                return result;
            }
        }
    }
}
