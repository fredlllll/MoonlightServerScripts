
namespace MoonlightDashboard.Database.Models
{
    public class Arma3ModsetMod:Model, IEquatable<Arma3ModsetMod?>
    {
        public required string ModsetId { get; set; }
        public required string ModSteamId { get; set; }

        public override bool Equals(object? obj)
        {
            return Equals(obj as Arma3ModsetMod);
        }

        public bool Equals(Arma3ModsetMod? other)
        {
            return other is not null &&
                   base.Equals(other) &&
                   ModsetId == other.ModsetId &&
                   ModSteamId == other.ModSteamId;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(base.GetHashCode(), ModsetId, ModSteamId);
        }

        public static bool operator ==(Arma3ModsetMod? left, Arma3ModsetMod? right)
        {
            return EqualityComparer<Arma3ModsetMod>.Default.Equals(left, right);
        }

        public static bool operator !=(Arma3ModsetMod? left, Arma3ModsetMod? right)
        {
            return !(left == right);
        }
    }
}
