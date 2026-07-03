using System.Reflection;

namespace MoonlightDashboard.Lib
{
    public static class PropertyMapper
    {
        public static T MapFromDictionary<T>(Dictionary<string, string> dictionary) where T : new()
        {
            T obj = new T();
            Type type = typeof(T);

            foreach (var kvp in dictionary)
            {
                // Find a property that matches the systemctl key (case-insensitive)
                FieldInfo? field = type.GetField(kvp.Key, BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase);

                if (field != null)
                {
                    try
                    {
                        // Convert the string value to the field's actual type
                        object convertedValue = Convert.ChangeType(kvp.Value, field.FieldType);

                        // Set the field value on our object
                        field.SetValue(obj, convertedValue);
                    }
                    catch
                    {
                        // Context-specific error handling/logging goes here
                    }
                }
            }

            return obj;
        }
    }
}
