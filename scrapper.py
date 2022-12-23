from requests import Session
import bs4
import re
from functools import lru_cache
from urllib3.exceptions import NewConnectionError

def get_countries(session : Session, 
                  url : str, 
                  cookie_url : str, 
                  country_url : str) -> list:    
    try:
        cookie = session.get(url + cookie_url)
        countries = session.get(url + country_url, cookies= cookie.cookies)
    except NewConnectionError as nce:
        print(nce)
        return []
    return countries.json()

def get_leaders_of_country(session : Session,
                           country_abv : str,
                           url : str,
                           cookie_url : str,
                           leaders_url : str) -> list:
    try:
        cookie = session.get(url + cookie_url)
        leaders = session.get(url + leaders_url,
                             params= {f"country": {country_abv}},
                             cookies= cookie.cookies)
        if leaders.status_code != 200:
            raise Exception(f"Error : Unable to get the leader of {country_abv}")
        else:
            return leaders.json()
    except NewConnectionError as nce:
        print(nce)
        return []
    except Exception as e:
        print(e)
        return[]
    
def get_leaders_of_country_first_paragraph(session : Session, 
                                           leaders : list) -> list:
    list_of_first_paragraph = []
    for leader in leaders:
        list_of_first_paragraph.append(get_first_paragraph(session,
                                                           leader['wikipedia_url']))
    return list_of_first_paragraph        
    
#@lru_cache(maxsize = None)
def get_first_paragraph(session : Session,
                        url : str):
    """Get the first paragraph of the wikipedia link given to it"""  
    req = session.get(url)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    for paragraph in soup.find_all('p'):
        for _ in paragraph.find_all('b'):
            #removing parenthese and what is between them
            first_paragraph = re.sub(" \([^()]+\)", '', paragraph.text)
            #removing url link
            first_paragraph = re.sub("(?P<url>https?://[^\s]+)", '', first_paragraph)
            return first_paragraph
    print(paragraph)
    return None
        
def get_leaders():
    """Get all the leaders of the five contries given by the API"""
    with Session() as session:
        
        url = "https://country-leaders.onrender.com/"
        country_url = "countries"
        cookie_url = "cookie"
        leaders_url = "leaders"
        leaders = []
        first_paragraphs = []
        
        countries = get_countries(session, 
                                  url, 
                                  cookie_url, 
                                  country_url)
        for country in countries:
            leaders.append(get_leaders_of_country(session, 
                                                  country, 
                                                  url, 
                                                  cookie_url, 
                                                  leaders_url))
            
        leaders_per_country = {countries[0]: leaders[0],
                               countries[1]: leaders[1],
                               countries[2]: leaders[2],
                               countries[3]: leaders[3],
                               countries[4]: leaders[4]}
        for i in range(len(countries)):
            first_paragraphs.append(get_leaders_of_country_first_paragraph(session, 
                                                                           leaders[i]))
        return leaders_per_country
    
leaders_per_country = get_leaders()