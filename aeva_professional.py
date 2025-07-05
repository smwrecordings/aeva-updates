# aeva_professional.py

import json
import os


class AevaProfessionalModule:
    def __init__(self, profession_data_path="assets/data/professions.json"):
        self.profession_data_path = profession_data_path
        self.professions = {}
        self.load_professions()

    def load_professions(self):
        if os.path.exists(self.profession_data_path):
            with open(self.profession_data_path, 'r') as f:
                self.professions = json.load(f)
        else:
            self.professions = {
                "hvac": {
                    "description": "Handles heating, ventilation, and air conditioning systems.",
                    "tools": ["Multimeter", "Manifold gauge", "Vacuum pump", "Thermometer"],
                    "checklist": ["Inspect filters", "Check refrigerant levels", "Clean condenser coils"]
                },
                "mechanic": {
                    "description": "Repairs and maintains vehicles and machinery.",
                    "tools": ["Socket wrench", "OBD scanner", "Torque wrench", "Hydraulic jack"],
                    "checklist": ["Check engine codes", "Inspect belts and hoses", "Test brakes"]
                },
                "electrician": {
                    "description": "Installs and repairs electrical systems.",
                    "tools": ["Wire stripper", "Voltage tester", "Fish tape", "Multimeter"],
                    "checklist": ["Check circuit breakers", "Test voltage", "Inspect grounding"]
                },
                "plumber": {
                    "description": "Installs and repairs water systems and fixtures.",
                    "tools": ["Pipe wrench", "Plunger", "Snake auger", "Teflon tape"],
                    "checklist": ["Inspect pipes for leaks", "Check water pressure", "Ensure proper drainage"]
                },
                "police": {
                    "description": "Maintains law and order, protects citizens.",
                    "tools": ["Radio", "Body cam", "Firearm", "Taser"],
                    "checklist": ["Check patrol car", "Inspect duty belt", "Review daily briefing"]
                }
            }

    def get_profession_info(self, title):
        return self.professions.get(
            title.lower(), {
                "description": "No data found for this profession."})

    def list_available_professions(self):
        return list(self.professions.keys())

    def diagnose_issue(self, profession, symptoms):
        # AI diagnostic logic placeholder
        return f"Based on your input in {profession}, the issue may involve: {
            ', '.join(symptoms)}. Recommended analysis engaged."

    def recommend_tools(self, profession):
        return self.professions.get(
            profession.lower(), {}).get(
            "tools", ["No tool data available."])

    def generate_checklist(self, profession):
        return self.professions.get(
            profession.lower(), {}).get(
            "checklist", ["No checklist available."])

    def simulate_scenario(self, profession, scenario):
        return f"Simulating {profession} scenario: {scenario}... Outcome: AI analysis in progress."


# Example usage:
if __name__ == "__main__":
    apm = AevaProfessionalModule()
    print("Available professions:", apm.list_available_professions())
    print(apm.get_profession_info("hvac"))
    print(
        apm.diagnose_issue(
            "hvac", [
                "no airflow", "high energy consumption"]))
    print(apm.recommend_tools("hvac"))
    print(apm.generate_checklist("hvac"))
