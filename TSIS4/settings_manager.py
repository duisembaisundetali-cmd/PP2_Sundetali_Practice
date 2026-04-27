import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "snake_color": [0, 255, 0],
            "grid_overlay": False,
            "sound": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.default_settings.copy()
        else:
            self.save_settings(self.default_settings)
            return self.default_settings.copy()
    
    def save_settings(self, settings):
        """Save settings to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(settings, f, indent=4)
            print("Settings saved successfully")
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key):
        """Get setting value"""
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
        self.save_settings(self.settings)
    
    def update(self, new_settings):
        """Update multiple settings"""
        self.settings.update(new_settings)
        self.save_settings(self.settings)