import requests
import re
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="get_city_name")

url = "https://uk-air.defra.gov.uk/latest/currentlevels?view=site"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

result = requests.get(url,headers=headers)
soup = BeautifulSoup(result.text,'lxml')

links = []
for link in soup.find_all('a', attrs={'href': re.compile("../networks/site-info")}):
    links.append(link.get('href'))

full_links = []
for link in links:
    full_link = link.replace('..', 'http://uk-air.defra.gov.uk')
    full_links.append(full_link)

for full_link in full_links:
    site_id = full_link.replace('http://uk-air.defra.gov.uk/networks/site-info?site_id=', '')
    result2 = requests.get(full_link,headers=headers)
    soup2 = BeautifulSoup(result2.text,'lxml')

    uk_air_id = soup2.find(text=re.compile("UK-AIR ID:")).find_parent("p").get_text().replace("UK-AIR ID: ","")
    eu_site_id = soup2.find(text=re.compile("EU Site ID:")).find_parent("p").get_text().replace("EU Site ID: ","")
    region = soup2.find(text=re.compile("Government Region:")).find_parent("p").get_text().replace("Government Region: ","")
    coordinates = soup2.find(text=re.compile("Latitude/Longitude:")).find_parent("p").get_text().replace("Latitude/Longitude: ","")
    latitude,longitude = coordinates.split(', ')

    h1 = soup2.find_all(string=re.compile("Site Information for"))[0]
    name = h1.split("(")[0].replace('    Site Information for ', '')

    worldlocation = geolocator.reverse(coordinates, exactly_one=True)
    address = worldlocation.raw['address']
    city = address.get('city', '')

    print(uk_air_id + ',' + eu_site_id + ',' + site_id + ',' + name + ',' + city + ',' + region + ',' + latitude + ',' + longitude)