import json
import os
from datetime import datetime

class PersistenceManager:
    @staticmethod
    def load_settings():
        """Load settings from settings.json"""
        default_settings = {
            'sound': True,
            'car_color': (0, 255, 0),  # Green
            'difficulty': 'Medium'
        }
        
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    data = json.load(f)
                    # Convert color from list to tuple
                    if 'car_color' in data and isinstance(data['car_color'], list):
                        data['car_color'] = tuple(data['car_color'])
                    # Ensure all keys exist
                    for key in default_settings:
                        if key not in data:
                            data[key] = default_settings[key]
                    return data
            except Exception as e:
                print(f"Error loading settings: {e}")
                return default_settings
        return default_settings
    
    @staticmethod
    def save_settings(settings):
        """Save settings to settings.json"""
        save_settings = settings.copy()
        if 'car_color' in save_settings and isinstance(save_settings['car_color'], tuple):
            save_settings['car_color'] = list(save_settings['car_color'])
        
        with open('settings.json', 'w') as f:
            json.dump(save_settings, f, indent=4)
    
    @staticmethod
    def load_leaderboard():
        """Load leaderboard from leaderboard.json"""
        if os.path.exists('leaderboard.json'):
            try:
                with open('leaderboard.json', 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    @staticmethod
    def save_score(name, score, distance):
        """Save a new score to the leaderboard"""
        leaderboard = PersistenceManager.load_leaderboard()
        
        leaderboard.append({
            'name': name,
            'score': score,
            'distance': distance,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:10]
        
        with open('leaderboard.json', 'w') as f:
            json.dump(leaderboard, f, indent=4)