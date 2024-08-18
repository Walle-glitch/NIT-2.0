import requests
from bs4 import BeautifulSoup
import paramiko
import _Router_Conf
import time

######### GET AN RFC ######### 
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

# Funktion för att konfigurera BGP på en specifik router
def configure_bgp_neighbor(neighbor_ip, neighbor_as):
    router_ip = _Router_Conf.ROUTER_IP
    username = _Router_Conf.ROUTER_USERNAME
    password = _Router_Conf.ROUTER_PASSWORD
    
    # Skapa SSH-klienten
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Anslut till routern
        ssh.connect(router_ip, username=username, password=password)
        
        # Öppna en shell-session
        remote_conn = ssh.invoke_shell()

        # Vänta lite så att sessionen initieras
        remote_conn.recv(1000)
        
        # Skicka kommandon till routern för att konfigurera BGP
        commands = [
            "enable",  # Anta att inget lösenord krävs för enable-läget
            "configure terminal",
            f"router bgp 64512",
            f"neighbor {neighbor_ip} remote-as {neighbor_as}",
            f"neighbor {neighbor_ip} ebgp-multihop 30",
            f"neighbor {neighbor_ip} update-source GigabitEthernet0/0",
            f"address-family ipv4",
            f"neighbor {neighbor_ip} activate",
            "exit-address-family",
            "exit",
            "interface gi0/0",
            "do show ip interface brief | include GigabitEthernet0/0",
            "do show running-config | include router bgp"
        ]

        output = ""
        for cmd in commands:
            remote_conn.send(cmd + "\n")
            time.sleep(1)  # Vänta på att kommandot ska exekveras
            output += remote_conn.recv(5000).decode("utf-8")
        
        # Extrahera information om IP-adress och befintligt AS-nummer
        interface_output = output.splitlines()
        gi0_ip = ""
        as_number = ""
        for line in interface_output:
            if "GigabitEthernet0/0" in line:
                gi0_ip = line.split()[1]  # Extrahera IP-adressen från rätt rad
            if "router bgp" in line:
                as_number = line.split()[2]  # Extrahera AS-numret från rätt rad
        
        return gi0_ip, as_number

    except Exception as e:
        # Hantera eventuella fel som kan uppstå
        return str(e), None

    finally:
        # Stäng SSH-anslutningen oavsett om det gick bra eller inte
        ssh.close()
