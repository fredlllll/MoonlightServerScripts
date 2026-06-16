using System.Security.Cryptography;
using System.Text;

namespace MoonlightDashboard.Lib
{
    public static class PassHash
    {
        public static string HashPassword(string password, string salt, int iterations=10000)
        {
            var saltBytes = Convert.FromBase64String(salt);
            using var pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, iterations, HashAlgorithmName.SHA256);
            return Convert.ToBase64String(pbkdf2.GetBytes(32)); // 32-byte hash
        }

        public static string GenerateSalt(int size = 16)
        {
            var saltBytes = RandomNumberGenerator.GetBytes(size);
            return Convert.ToBase64String(saltBytes);
        }

        public static bool VerifyPassword(string password, string storedHash, string storedSalt, int iterations=10000)
        {
            // 1. Convert stored strings back to byte arrays
            var saltBytes = Convert.FromBase64String(storedSalt);
            var hashBytes = Convert.FromBase64String(storedHash);

            // 2. Re-calculate the hash using the same parameters
            using var pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, iterations, HashAlgorithmName.SHA256);
            var inputHash = pbkdf2.GetBytes(32); // Must match the original byte length (32)

            // 3. Constant-time comparison to prevent timing attacks
            return CryptographicOperations.FixedTimeEquals(inputHash, hashBytes);
        }
    }
}
