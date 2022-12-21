import requests

def get_leaders():
    url = "https://country-leaders.onrender.com/"
    status_url = "status"
    country_url = "countries"
    cookie_url = "cookie"
    leaders_url = "leaders"
    leaders = []
    
    cookie = requests.get(url + cookie_url)
    countries = requests.get(url + country_url, 
                         cookies= cookie.cookies).json()
    for country in countries:
        cookie = requests.get(url + cookie_url)
        leaders.append(requests.get(url + leaders_url,
                               params= {f"country": {country}},
                               cookies= cookie.cookies).json())
    leaders_per_country = {countries[0]: leaders[0],
                           countries[1]: leaders[1],
                           countries[2]: leaders[2],
                           countries[3]: leaders[3],
                           countries[4]: leaders[4]}
    return leaders_per_country


req = requests.get(url + status_url)
if req.status_code == 200:
    print(f"Request to {url}/{status_url} was succesfull!")
else:
    print(f"A problem has occured during the request to {url}/{status_url}!")