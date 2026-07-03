using System.Security.Cryptography;
using System.Text;

namespace MoonlightDashboard.Lib
{
    public static class PassHash
    {
        public static string HashPassword(string password)
        {
            int saltSize = 16;
            int iterations = 10000;
            var salt = GenerateSalt(saltSize);
            var hash = HashPassword(password, salt, iterations);
            return $"{saltSize}:{salt}:{iterations}:{hash}"; 
        }

        public static bool VerifyPassword(string password, string storedHash)
        {
            var parts = storedHash.Split(':');
            if (parts.Length != 4) return false;
            int saltSize = int.Parse(parts[0]);
            string salt = parts[1];
            int iterations = int.Parse(parts[2]);
            string hash = parts[3];
            return VerifyPassword(password, hash, salt, iterations);
        }


        private static string HashPassword(string password, string salt, int iterations)
        {
            var saltBytes = Convert.FromBase64String(salt);
            using var pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, iterations, HashAlgorithmName.SHA256);
            return Convert.ToBase64String(pbkdf2.GetBytes(32)); // 32-byte hash
        }

        private static string GenerateSalt(int size)
        {
            var saltBytes = RandomNumberGenerator.GetBytes(size);
            return Convert.ToBase64String(saltBytes);
        }

        private static bool VerifyPassword(string password, string storedHash, string storedSalt, int iterations)
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
