# aeva_starlink.py

import os
import json
import time
import requests
from datetime import datetime


class AevaStarlink:
    def __init__(self, starlog_path="assets/data/starlink_log.json"):
        self.starlog_path = starlog_path
        os.makedirs(os.path.dirname(starlog_path), exist_ok=True)
        self.log = []

    def _save_log(self):
        with open(self.starlog_path, "w") as f:
            json.dump(self.log, f, indent=4)

    def log_event(self, label, data=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "label": label,
            "data": data or {}
        }
        self.log.append(entry)
        self._save_log()
        print(f"[AevaStarlink] {label} logged.")

    def fetch_satellite_data(self):
        print("[AevaStarlink] Fetching satellite telemetry (public API)...")
        try:
            res = requests.get(
                "https://api.wheretheiss.at/v1/satellites/25544",
                timeout=5)
            if res.status_code == 200:
                data = res.json()
                self.log_event("ISS_Position", data)
                print(
                    f"[AevaStarlink] ISS Location: Lat {
                        data['latitude']} Lon {
                        data['longitude']}")
                return data
        except Exception as e:
            print(f"[AevaStarlink] Error: {e}")
            return None

    def fetch_starlink_status(self):
        print("[AevaStarlink] Attempting Starlink constellation data fetch...")
        try:
            response = requests.get(
                "https://satellitemap.space/api/v1/satellites", timeout=5)
            if response.status_code == 200:
                sats = response.json()
                self.log_event(
                    "StarlinkConstellation", {
                        "satellites_tracked": len(sats)})
                print(
                    f"[AevaStarlink] Tracked Starlink Satellites: {
                        len(sats)}")
                return sats
        except Exception:
            print("[AevaStarlink] Starlink data unavailable.")
            return []

    def track_gps_position(self, lat, lon):
        print(
            f"[AevaStarlink] GPS tracking requested for lat {lat}, lon {lon}...")
        try:
            url = f"https://api.weather.gov/points/{lat},{lon}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                info = res.json()
                forecast_url = info['properties']['forecast']
                forecast = requests.get(forecast_url).json()
                self.log_event("GPSForecast", forecast)
                print("[AevaStarlink] Weather forecast retrieved and logged.")
                return forecast
        except Exception as e:
            print(f"[AevaStarlink] Error: {e}")
            return None


# Example usage
if __name__ == "__main__":
    star = AevaStarlink()
    star.fetch_satellite_data()
    star.fetch_starlink_status()
    star.track_gps_position(34.0522, -118.2437)  # Example: Los Angeles
