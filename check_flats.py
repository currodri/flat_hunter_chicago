import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def load_params():
    with open('search_params.json', 'r') as f:
        return json.load(f)

def check_flats(move_in_date):
    url = "https://1130smichigan.com/available-residences/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the form and set the move-in date
    form = soup.find('form', id='search-form')
    if form:
        form_data = {
            'move_in_date': move_in_date
        }
        # Submit the form with the move-in date
        response = requests.post(url, data=form_data)
        soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Find all available flats
    flats = soup.find_all('div', class_='floor-plan')
    available_flats = [flat.text for flat in flats if 'Available' in flat.text]
    
    return available_flats

def update_readme(available_flats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('README.md', 'w') as f:
        f.write("# Available Flats\n\n")
        f.write(f"Last updated: {now}\n\n")
        if available_flats:
            for flat in available_flats:
                f.write(f"- {flat}\n")
        else:
            f.write("No flats available at the moment.\n")

if __name__ == "__main__":
    params = load_params()
    move_in_date = params.get('move_in_date', '2024-10-15')
    available_flats = check_flats(move_in_date)
    update_readme(available_flats)
    print("README.md updated with available flats.")
