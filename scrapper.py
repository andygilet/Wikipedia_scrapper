import requests
import bs4
import re

def get_leaders():
    """Get all the leaders of the five contries given by the API"""
    url = "https://country-leaders.onrender.com/"
    country_url = "countries"
    cookie_url = "cookie"
    leaders_url = "leaders"
    leaders = []
    
    try:
        cookie = requests.get(url + cookie_url)
        countries = requests.get(url + country_url, 
                             cookies= cookie.cookies)
        if countries.status_code != 200:
            raise Exception("Error : Unable to get the countries name !")
    except Exception as e:
        print(e)
        return None
    countries = countries.json()
    
    for country in countries:
        try:
            cookie = requests.get(url + cookie_url)
            leader = requests.get(url + leaders_url,
                                    params= {f"country": {country}},
                                    cookies= cookie.cookies)
            if leader.status_code != 200:
                raise Exception(f"Error : Unable to get the leader of {country}")
        except Exception as e:
            print(e)
            leader = None
        leaders.append(leader)
        
    leaders_per_country = {countries[0]: leaders[0],
                           countries[1]: leaders[1],
                           countries[2]: leaders[2],
                           countries[3]: leaders[3],
                           countries[4]: leaders[4]}
    return leaders_per_country

def get_first_paragraph(url):
    """Get the first paragraph of the wikipedia link given to it"""
    print(f"Getting the first paragraph of : {url}")
    
    try:
        req = requests.get(url)
        if req.status_code != 200:
            raise Exception(f"Error : Unable to access {url}")
    except Exception as e:
        print(e)
        return None
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    for paragraph in soup.find_all('p'):
        if paragraph.find_all('b'):
            #removing parenthese and what is between them
            first_paragraph = re.sub(" \([^()]+\)", '', paragraph.text)
            #removing url link
            first_paragraph = re.sub("(?P<url>https?://[^\s]+)", '', first_paragraph)
            return first_paragraph