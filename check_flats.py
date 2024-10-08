import requests
from bs4 import BeautifulSoup
from datetime import datetime

def check_flats():
    url = "https://1130smichigan.com/floor-plans/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Find all available flats
    flats = soup.find_all('div', class_='floor_plan')
    available_flats = [flat.text for flat in flats if 'Available' in flat.text]
    
    return available_flats

def update_readme(available_flats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('README.md','w') as f:
        f.write("# Available Flats\n\n")
        f.write(f"Last updated: {now}\n\n")
        if available_flats:
            for flat in available_flats:
                f.write(f"- {flat}\n")
        else:
            f.write("No flats available at the moment.\n")


if __name__ == "__main__":
    available_flats = check_flats()
    update_readme(available_flats)
    print("README.md updated with available flats.")