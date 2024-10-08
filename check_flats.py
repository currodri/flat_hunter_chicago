import requests
import json
from datetime import datetime

def load_params():
    with open('search_params.json', 'r') as f:
        return json.load(f)

def check_flats(move_in_date,rent_min):
    api_url = "https://1130smichigan.com/wp-json/floorplans/v1/available-units"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 403:
        print("Access denied. Check if the website is blocking your requests.")
        return []

    data = response.json()
    available_flats = []

    for floor_plan in data['posts']:
        if '1BR/1BA' in floor_plan['name']:
            for unit in floor_plan['available_units']:
                if unit['available'] >= move_in_date and int(unit['rent_min']) <= rent_min:
                    available_flats.append({
                    'floor_plan_name': unit['floor_plan_name'],
                    'unit_number': unit['unit_number'],
                    'sqft': unit['sqft'],
                    'rent_min': unit['rent_min'],
                    'rent_max': unit['rent_max'],
                    'available': unit['available'],
                    'apply_url': unit['apply_url']
                })
    
    return available_flats

def update_readme(available_flats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('README.md', 'w') as f:
        f.write("# Available Flats\n\n")
        f.write(f"**Last updated:** {now}\n\n")
        if available_flats:
            f.write("## Flats Available:\n")
            for flat in available_flats:
                f.write(f"### {flat['floor_plan_name']} (Unit {flat['unit_number']})\n")
                f.write(f"- **Square Feet:** {flat['sqft']} sqft\n")
                f.write(f"- **Rent:** ${flat['rent_min']} - ${flat['rent_max']}\n")
                f.write(f"- **Available From:** {flat['available']}\n")
                f.write(f"- Apply Here\n\n")
        else:
            f.write("No flats available at the moment.\n")

if __name__ == "__main__":
    params = load_params()
    move_in_date = params.get('move_in_date', '01/01/2025')
    rent_min = params.get('rent_min', '2000')
    available_flats = check_flats(move_in_date,rent_min)
    update_readme(available_flats)
    print("README.md updated with available flats.")
