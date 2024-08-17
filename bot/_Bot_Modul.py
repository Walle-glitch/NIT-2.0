# Use this on for Fun Functions!

# GET AN RFC
import requests
from bs4 import BeautifulSoup

def get_rfc(rfc_number):
    """
    Hämtar RFC från IETF:s datatracker baserat på RFC-nummer.
    
    :param rfc_number: RFC-nummer som ska hämtas.
    :return: En sträng med RFC:s titel och länk.
    """
    # Bygg URL till RFC
    url = f"https://datatracker.ietf.org/doc/html/rfc{rfc_number}"
    
    try:
        # Skicka en HTTP GET-förfrågan
        response = requests.get(url)
        response.raise_for_status()  # Kasta ett undantag om statuskod är 4xx eller 5xx
        
        # Använd BeautifulSoup för att parsa HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Hämta RFC-titel från HTML
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text
        else:
            title = "RFC-titel kunde inte hittas."

        # Returnera RFC-titel och länk
        return f"{title}\nLänk: {url}"
    
    except requests.RequestException as e:
        # Hantera eventuella HTTP-fel
        return f"Fel vid hämtning av RFC: {e}"
