from requests import Session
import bs4
import re
from functools import lru_cache

@lru_cache(maxsize = None)
def get_first_paragraph(url : str, session : Session):
    """Get the first paragraph of the wikipedia link given to it"""
    
    try:
        req = session.get(url)
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
        else:
            print("First paragraph not found !")
            return None

def get_leaders():
    """Get all the leaders of the five contries given by the API"""
    with Session() as session:
        
        url = "https://country-leaders.onrender.com/"
        country_url = "countries"
        cookie_url = "cookie"
        leaders_url = "leaders"
        leaders = []
    
        try:
            cookie = session.get(url + cookie_url)
            countries = session.get(url + country_url, 
                                 cookies= cookie.cookies)
            if countries.status_code != 200:
                raise Exception("Error : Unable to get the countries name !")
        except Exception as e:
            print(e)
            return None
        countries = countries.json()
    
        for country in countries:
            try:
                cookie = session.get(url + cookie_url)
                leader = session.get(url + leaders_url,
                                        params= {f"country": {country}},
                                        cookies= cookie.cookies)
                if leader.status_code != 200:
                    raise Exception(f"Error : Unable to get the leader of {country}")
                else:
                    for l in leader.json():
                        print(l['wikipedia_link'])
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