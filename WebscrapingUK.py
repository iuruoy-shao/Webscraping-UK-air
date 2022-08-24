import requests
import re
from bs4 import BeautifulSoup

url="https://uk-air.defra.gov.uk/latest/currentlevels?view=site"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

result = requests.get(url,headers=headers)
soup = BeautifulSoup(result.text,'html')

links = []
for link in soup.findAll('a', attrs={'href': re.compile("../networks/site-info")}):
    links.append(link.get('href'))

full_links=[]
for link in links:
  full_link = link.replace('..', 'http://uk-air.defra.gov.uk')
  full_links.append(full_link)

result_test = requests.get('http://uk-air.defra.gov.uk/networks/site-info?site_id=ABD',headers=headers)
soup_test = BeautifulSoup(result_test.text,'html')

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

for full_link in full_links:
  site_id = full_link.replace('http://uk-air.defra.gov.uk/networks/site-info?site_id=', '')
  result2 = requests.get(full_link,headers=headers)
  soup2 = BeautifulSoup(result2.text,'html')

  list_uk_air_id = soup2.find_all(string=re.compile("UKA"))
  uk_air_id = (list_uk_air_id[2]).replace(' ','')

  list_eu_site_id = soup_test.find_all(string=re.compile("GB"))
  eu_site_id = (list_eu_site_id[0]).replace(' ','')

  list_name = soup2.find_all(string=re.compile("Site Information for"))
  fullname = list_name[0]

  fullname2,b = fullname.split("(")
  name = fullname2.replace('    Site Information for ', '')

  list_region = soup2.findAll('p')
  regionfull = "".join(str(list_region))
  regionfull2,c = regionfull.split('<p><strong>Easting/Northing:</strong> ')
  d,region2 = regionfull2.split('<p><strong>Government Region:</strong> ')
  region = region2.replace('</p>, ','')
    
  e,locationfull = regionfull.split('<p><strong>Latitude/Longitude:</strong> ')
  locationfull2 = locationfull.split('</p>, <p>')
    
  coordinates = locationfull2[0]
  latitude,longitude = coordinates.split(', ')
  worldlocation = geolocator.reverse(coordinates, exactly_one=True)
  address = worldlocation.raw['address']
  city = address.get('city', '')

  if city == '':
    print(uk_air_id + ',' + eu_site_id + ',' + site_id + ',' + name + ',' + city + ',' + region + ',' + latitude + ',' + longitude)
