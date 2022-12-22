import requests
import bs4
import re

def get_leaders():
    url = "https://country-leaders.onrender.com/"
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

def get_first_paragraph(url):
    print(f"Getting the first paragraph of : {url}")
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    for paragraph in soup.find_all('p'):
        if paragraph.find_all('b'):
            first_paragraph = re.sub(" \([^()]+\)", '', paragraph.text)
            first_paragraph = re.sub("(?P<url>https?://[^\s]+)", '', first_paragraph)
            return first_paragraph