# Use this on for Fun Functions!

######### GET AN RFC ######### 
import requests
from bs4 import BeautifulSoup

def get_rfc(rfc_number):
    """
    Hämtar RFC från IETF:s datatracker baserat på RFC-nummer.
    
    :param rfc_number: RFC-nummer som ska hämtas.
    :return: En sträng med RFC:s titel och länk eller ett felmeddelande.
    """
    if not isinstance(rfc_number, int) or rfc_number <= 0:
        return "Fel: Ogiltigt RFC-nummer. Vänligen ange ett positivt heltal."
    
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
        if title_tag and "RFC" in title_tag.text:
            title = title_tag.text
        else:
            title = "RFC-titel kunde inte hittas eller det angivna RFC-numret är ogiltigt."

        # Returnera RFC-titel och länk
        return f"{title}\nLänk: {url}"
    
    except requests.RequestException as e:
        # Hantera eventuella HTTP-fel
        return f"Fel vid hämtning av RFC: {e}"

#############################################

import paramiko
import time
import _Router_Conf  # Hämtar användarnamn och lösenord från denna modul

def configure_bgp_neighbor(router_ip, bgp_neighbor_ip, bgp_as_number, neighbor_as_number):
    """
    Konfigurerar en BGP-nabo på en Cisco-router via SSH.
    
    :param router_ip: IP-adressen till Cisco-routern
    :param bgp_neighbor_ip: IP-adressen till BGP-nabon
    :param bgp_as_number: Det lokala AS-numret för BGP
    :param neighbor_as_number: AS-numret för BGP-nabon
    :return: Sträng med nödvändig information om BGP-konfigurationen
    """
    
    username = _Router_Conf.SSH_USERNAME
    password = _Router_Conf.SSH_PASSWORD
    
    # Skapa en SSH-klient
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Anslut till routern via SSH
        ssh_client.connect(hostname=router_ip, username=username, password=password)
        
        # Starta en interaktiv session
        remote_conn = ssh_client.invoke_shell()
        
        # Vänta lite för att få ett skal
        time.sleep(1)
        
        # Töm utgångsbuffer
        output = remote_conn.recv(65535)
        
        # Gå in i privilegierat läge
        remote_conn.send("enable\n")
        time.sleep(1)
        remote_conn.send(password + "\n")
        time.sleep(1)
        
        # Gå in i global konfigurationsläge
        remote_conn.send("configure terminal\n")
        time.sleep(1)
        
        # Konfigurera BGP
        remote_conn.send(f"router bgp {bgp_as_number}\n")
        time.sleep(1)
        remote_conn.send(f"neighbor {bgp_neighbor_ip} remote-as {neighbor_as_number}\n")
        time.sleep(1)
        
        # Slutför konfigurationen
        remote_conn.send("end\n")
        time.sleep(1)
        
        # Samla och returnera utgångsdata
        output = remote_conn.recv(65535).decode('utf-8')
        
        # Stäng anslutningen
        ssh_client.close()
        
        return f"BGP-peering har konfigurerats med nabon {bgp_neighbor_ip} i AS {neighbor_as_number}.\n\nUtgång:\n{output}"
    
    except Exception as e:
        return f"Ett fel inträffade: {str(e)}"


