import csv
import requests
from bs4 import BeautifulSoup

def hospital_about(name):
    url = f'https://airomedical.com/hospitals/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        about = soup.find('div', class_='AboutBlock_message__oiMr8').text.strip()
        return about
    else:
        return ''

def scrape_hospitals(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        hospitals = soup.find_all('div', class_='HospitalCard_infoContainer__9gvi1')
        hospital_data = []
        for hospital in hospitals:
            name = hospital.find('h2', class_="HospitalCard_name__UZRIa oneLine" ,itemprop="name").text.strip()
            address = hospital.find('span', itemprop="addressLocality").text.strip()
            country = hospital.find('span', itemprop="addressCountry").text.strip()
            about = hospital_about(str(name).lower().replace(" ", "-"))
            hospital_data.append({
                'Hospital Name': name,
                'Address': f'{address}, {country}',
                'About the Hospital': f'{about}',
            })
        return hospital_data
    else:
        print("Failed to retrieve data from the website.")
        return []
    
def doctor_about(name):
    url = f'https://airomedical.com/doctors/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        about = soup.find('div', class_='AboutBlock_message__oiMr8').text.strip()
        return about
    else:
        return ''
    
def scrape_doctors(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        doctors = soup.find_all('div', class_='DoctorPaginationCard_container__QCeN5')
        doctor_data = []
        for doctor in doctors:
            name = doctor.find('h2', class_="DoctorCard_name__05xCl", itemprop="name").text.strip()
            clean_name = str(name).lower().replace(".", "")
            about = doctor_about(str(clean_name).lower().replace(" ", "-"))
            doctor_data.append({
                'Doctor Name': name,
                'About': about,
            })
        return doctor_data 
    else:
        print("Failed to retrieve data from the website.")
        return []

def write_to_csv(filename, data):
    headers = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    hospitals_url = "https://airomedical.com/hospitals"
    doctors_url = "https://airomedical.com/doctors"
    
    print("Scraping hospital data...")
    hospital_data = scrape_hospitals(hospitals_url)
    if hospital_data:
        print(f"Scraped data for {len(hospital_data)} hospitals.")
        write_to_csv("hospital_data.csv", hospital_data)
    else:
        print("No hospital data scraped.")
    
    print("\nScraping doctor data...")
    doctor_data = scrape_doctors(doctors_url)
    if doctor_data:
        print(f"Scraped data for {len(doctor_data)} doctors.")
        write_to_csv("doctor_data.csv", doctor_data)
    else:
        print("No doctor data scraped.")
