import requests
import telnetlib
from bs4 import BeautifulSoup
import paramiko
import _Router_Conf
import time

######### GET AN RFC ######### 
def get_rfc(rfc_number):
    """
    Retrieves an RFC from the IETF data tracker based on RFC number.
    
    :param rfc_number: The RFC number to retrieve.
    :return: A string with the RFC title and link, or an error message.
    """
    if not isinstance(rfc_number, int) or rfc_number <= 0:
        return "Error: Invalid RFC number. Please provide a positive integer."
    
    # Build the URL for the RFC
    url = f"https://datatracker.ietf.org/doc/html/rfc{rfc_number}"
    
    try:
        # Send an HTTP GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for status codes 4xx or 5xx
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the RFC title from the HTML
        title_tag = soup.find('title')
        if title_tag and "RFC" in title_tag.text:
            title = title_tag.text
        else:
            title = "RFC title could not be found or the provided RFC number is invalid."

        # Return the RFC title and link
        return f"{title}\nLink: {url}"
    
    except requests.RequestException as e:
        # Handle any HTTP errors
        return f"Error retrieving RFC: {e}"

#############################################

# Function to configure BGP on a specific router
def configure_bgp_neighbor(neighbor_ip, neighbor_as):
    router_ip = _Router_Conf.ROUTER_IP
    username = _Router_Conf.SSH_USERNAME
    password = _Router_Conf.SSH_PASSWORD
    
    try:
        # Connect to the router via Telnet
        tn = telnetlib.Telnet(router_ip)

        # Log in with username and password
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        # Wait for the prompt
#        tn.read_until(b">")
        
        # Send commands to configure BGP
        commands = [
            "enable",  # Assuming no enable password is needed
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
            tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(1)  # Wait for the command to execute
            output += tn.read_very_eager().decode('ascii')

        # Extract information about IP address and existing AS number
        interface_output = output.splitlines()
        gi0_ip = ""
        as_number = ""
        for line in interface_output:
            if "GigabitEthernet0/0" in line:
                gi0_ip = line.split()[1]  # Extract the IP address from the correct line
            if "router bgp" in line:
                as_number = line.split()[2]  # Extract the AS number from the correct line

        return gi0_ip, as_number

    except Exception as e:
        # Handle any errors that might occur
        return f"An error occurred: {str(e)}", None

    finally:
        # Close the Telnet connection
        tn.write(b"exit\n")
        tn.close()
