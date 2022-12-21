import requests

url = "https://country-leaders.onrender.com/"
status_url = "status"
country_url = "countries"
cookie_url = "cookie"
leaders_url = "leaders"

leaders = []

req = requests.get(url + status_url)
if req.status_code == 200:
    print(f"Request to {url}/{status_url} was succesfull!")
else:
    print(f"A problem has occured during the request to {url}/{status_url}!")
    
cookies = requests.get(url + cookie_url)
countries = requests.get(url + country_url, 
                         cookies= cookies.cookies)
if countries.status_code == 200:
    print(countries.json())
    
for country in countries.json():
    cookies = requests.get(url + cookie_url)
    leaders = requests.get(url + leaders_url,
                           params= {f"country": {country}},
                           cookies= cookies.cookies)
if leaders.status_code == 200:
    print(leaders.json())
    print("\n")
else:
    print(leaders.status_code)
