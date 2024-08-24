# This is _Network_Tech_Game.py

import random

# List of questions, each with options and the index of the correct option
questions = [
    {
        "question": "What does VLAN stand for?",
        "options": ["Virtual Local Area Network", "Very Large Area Network", "Variable Local Area Network", "Virtual Light Area Network"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol is used for secure communication over the internet?",
        "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
        "correct_option_index": 2
    },
    {
        "question": "What is the purpose of the DHCP protocol?",
        "options": ["Assign IP addresses dynamically", "Translate domain names to IP addresses", "Secure data transfer", "Route packets between networks"],
        "correct_option_index": 0
    },
    {
        "question": "Which layer of the OSI model does a switch operate at?",
        "options": ["Layer 1", "Layer 2", "Layer 3", "Layer 4"],
        "correct_option_index": 1
    },
    {
        "question": "What is the main function of the ARP protocol?",
        "options": ["Translate domain names to IP addresses", "Resolve IP addresses to MAC addresses", "Encrypt data packets", "Establish TCP connections"],
        "correct_option_index": 1
    },
    {
        "question": "What does the acronym OSPF stand for?",
        "options": ["Open Shortest Path First", "Open Source Path Finder", "Optimal Shortest Path Forwarding", "Open Source Protocol Framework"],
        "correct_option_index": 0
    },
    {
        "question": "Which layer of the OSI model does the IP protocol operate on?",
        "options": ["Layer 2", "Layer 3", "Layer 4", "Layer 5"],
        "correct_option_index": 1
    },
    {
        "question": "In which protocol is the TTL (Time To Live) field used?",
        "options": ["ICMP", "UDP", "TCP", "IP"],
        "correct_option_index": 3
    },
    {
        "question": "What does NAT stand for in networking?",
        "options": ["Network Address Translation", "Network Access Technology", "Network Address Testing", "Network Automatic Translation"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol is used for encrypting data in a VPN?",
        "options": ["PPTP", "L2TP", "IPsec", "GRE"],
        "correct_option_index": 2
    },
    {
        "question": "What is the default administrative distance of OSPF?",
        "options": ["90", "100", "110", "120"],
        "correct_option_index": 2
    },
    {
        "question": "What is the purpose of a VLAN?",
        "options": ["To segment broadcast domains", "To create multiple routing paths", "To manage IP address allocation", "To provide encryption for data"],
        "correct_option_index": 0
    },
    {
        "question": "Which type of DNS record is used to map domain names to IP addresses?",
        "options": ["MX", "A", "CNAME", "PTR"],
        "correct_option_index": 1
    },
    {
        "question": "What does BGP stand for?",
        "options": ["Border Gateway Protocol", "Binary Gateway Protocol", "Basic Gateway Protocol", "Broadband Gateway Protocol"],
        "correct_option_index": 0
    },
    {
        "question": "What is the primary function of the ARP protocol?",
        "options": ["Translate IP addresses to MAC addresses", "Encrypt data packets", "Establish TCP connections", "Resolve domain names to IP addresses"],
        "correct_option_index": 0
    },
    {
        "question": "In the context of network security, what does IDS stand for?",
        "options": ["Intrusion Detection System", "Internal Data Security", "Internet Detection Service", "Integrated Defense System"],
        "correct_option_index": 0
    },
    {
        "question": "Which command is used to view the routing table on a Cisco router?",
        "options": ["show ip route", "show route", "view ip routing", "display routes"],
        "correct_option_index": 0
    },
    {
        "question": "Which layer of the OSI model does a hub operate on?",
        "options": ["Layer 1", "Layer 2", "Layer 3", "Layer 4"],
        "correct_option_index": 0
    },
    {
        "question": "What is the maximum length of a segment in Ethernet (in meters)?",
        "options": ["100 meters", "200 meters", "300 meters", "400 meters"],
        "correct_option_index": 0
    },
    {
        "question": "Which of the following is a routing protocol that uses distance-vector algorithms?",
        "options": ["OSPF", "EIGRP", "RIP", "BGP"],
        "correct_option_index": 2
    },
    {
        "question": "What type of network device connects multiple networks and routes packets between them?",
        "options": ["Switch", "Router", "Hub", "Modem"],
        "correct_option_index": 1
    },
    {
        "question": "What does the acronym VPN stand for?",
        "options": ["Virtual Private Network", "Variable Private Network", "Virtual Public Network", "Variable Public Network"],
        "correct_option_index": 0
    },
    {
        "question": "Which of the following protocols is used for network time synchronization?",
        "options": ["NTP", "FTP", "SNMP", "HTTP"],
        "correct_option_index": 0
    },
    {
        "question": "What is the purpose of the STP protocol?",
        "options": ["Prevent loops in a network", "Increase data transfer rate", "Encrypt data packets", "Provide redundancy"],
        "correct_option_index": 0
    },
    {
        "question": "Which command is used to display the current configuration on a Cisco device?",
        "options": ["show running-config", "display configuration", "view config", "show config"],
        "correct_option_index": 0
    },
    {
        "question": "What is the purpose of a subnet mask?",
        "options": ["To define the network and host portions of an IP address", "To route packets between different networks", "To encrypt data in transit", "To assign IP addresses to devices"],
        "correct_option_index": 0
    },
    {
        "question": "What type of cable is used for connecting devices in a LAN over short distances?",
        "options": ["Fiber optic", "Coaxial", "Twisted pair", "Serial"],
        "correct_option_index": 2
    },
    {
        "question": "What is the main difference between TCP and UDP?",
        "options": ["TCP is connection-oriented, while UDP is connectionless", "TCP is faster than UDP", "UDP provides error-checking, while TCP does not", "TCP is used for broadcasting, while UDP is used for unicasting"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol uses port 80 by default?",
        "options": ["HTTP", "HTTPS", "FTP", "SMTP"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym DHCP stand for?",
        "options": ["Dynamic Host Configuration Protocol", "Dynamic Hypertext Configuration Protocol", "Domain Host Configuration Protocol", "Dynamic Hypertext Control Protocol"],
        "correct_option_index": 0
    },
    {
        "question": "In a Cisco router, which command is used to configure an IP address on an interface?",
        "options": ["ip address [address] [mask]", "set ip [address] [mask]", "config ip [address] [mask]", "address ip [address] [mask]"],
        "correct_option_index": 0
    },
    {
        "question": "What is the purpose of the DNS protocol?",
        "options": ["Translate domain names to IP addresses", "Encrypt data packets", "Resolve IP addresses to MAC addresses", "Establish VPN connections"],
        "correct_option_index": 0
    },
    {
        "question": "Which of the following is a class of IP address reserved for multicast communication?",
        "options": ["Class A", "Class B", "Class C", "Class D"],
        "correct_option_index": 3
    },
    {
        "question": "What is the purpose of a firewall in network security?",
        "options": ["To control incoming and outgoing network traffic", "To establish secure VPN connections", "To manage IP address assignments", "To provide wireless connectivity"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol provides dynamic IP address allocation?",
        "options": ["DHCP", "ARP", "ICMP", "RARP"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym VPN stand for?",
        "options": ["Virtual Private Network", "Variable Private Network", "Virtual Public Network", "Variable Public Network"],
        "correct_option_index": 0
    },
    {
        "question": "What layer of the OSI model does SSL/TLS operate on?",
        "options": ["Layer 5", "Layer 6", "Layer 7", "Layer 4"],
        "correct_option_index": 3
    },
    {
        "question": "Which command is used to verify the connectivity between two devices on a network?",
        "options": ["ping", "traceroute", "show ip route", "netstat"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym QoS stand for in networking?",
        "options": ["Quality of Service", "Queue of Servers", "Query of Systems", "Quick Operating Speed"],
        "correct_option_index": 0
    },
    {
        "question": "What is the default port number for HTTPS?",
        "options": ["80", "443", "21", "25"],
        "correct_option_index": 1
    },
    {
        "question": "Which device operates at Layer 2 of the OSI model?",
        "options": ["Router", "Switch", "Hub", "Firewall"],
        "correct_option_index": 1
    },
    {
        "question": "What is the maximum length of a cable segment in a 10BaseT Ethernet network?",
        "options": ["100 meters", "200 meters", "300 meters", "400 meters"],
        "correct_option_index": 0
    },
    {
        "question": "Which of the following protocols is used for network management?",
        "options": ["SNMP", "HTTP", "FTP", "SMTP"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym VPN stand for?",
        "options": ["Virtual Private Network", "Virtual Public Network", "Variable Private Network", "Virtual Private Node"],
        "correct_option_index": 0
    },
    {
        "question": "Which of the following is used to provide secure remote access to a network?",
        "options": ["VPN", "Firewall", "NAT", "Proxy Server"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym RIP stand for?",
        "options": ["Routing Information Protocol", "Reliable Information Protocol", "Routing Integrated Protocol", "Reliable Internet Protocol"],
        "correct_option_index": 0
    },
    {
        "question": "In which protocol is the SYN flag used?",
        "options": ["TCP", "UDP", "ICMP", "ARP"],
        "correct_option_index": 0
    },
    {
        "question": "Which command is used to view the interface status on a Cisco device?",
        "options": ["show interfaces", "view status", "show ip interface", "display interfaces"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol is used to automatically assign IP addresses to devices on a network?",
        "options": ["DHCP", "DNS", "NAT", "ARP"],
        "correct_option_index": 0
    },
    {
        "question": "What is the function of the ICMP protocol?",
        "options": ["Error reporting and diagnostic functions", "Encryption of data packets", "Routing of packets", "Dynamic IP address assignment"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym EIGRP stand for?",
        "options": ["Enhanced Interior Gateway Routing Protocol", "Enhanced Internet Gateway Routing Protocol", "Extended Integrated Gateway Routing Protocol", "Enhanced Interdomain Gateway Routing Protocol"],
        "correct_option_index": 0
    },
    {
        "question": "Which layer of the OSI model is responsible for end-to-end communication and error recovery?",
        "options": ["Layer 2", "Layer 3", "Layer 4", "Layer 5"],
        "correct_option_index": 2
    },
    {
        "question": "Which command is used to reload a Cisco device?",
        "options": ["reload", "reboot", "restart", "reset"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym AAA stand for in network security?",
        "options": ["Authentication, Authorization, and Accounting", "Automatic Access and Authorization", "Advanced Authentication and Accounting", "Automatic Authentication and Access"],
        "correct_option_index": 0
    },
    {
        "question": "What is the primary purpose of a proxy server?",
        "options": ["To act as an intermediary between clients and servers", "To provide secure remote access", "To route packets between networks", "To manage IP address assignments"],
        "correct_option_index": 0
    },
    {
        "question": "Which protocol is used to secure communication between a web server and a browser?",
        "options": ["HTTPS", "HTTP", "FTP", "Telnet"],
        "correct_option_index": 0
    },
    {
        "question": "What does the acronym MPLS stand for?",
        "options": ["Multi-Protocol Label Switching", "Multi-Protocol Local Switching", "Maximum Protocol Label Switching", "Multi-Protocol Layer Switching"],
        "correct_option_index": 0
    }
]

# Dictionary to keep track of scores for each user
user_scores = {}

def generate_question():
    """
    Generates a random network-related question with options.
    
    :return: A tuple containing the question, options, and index of the correct answer.
    """
    question = random.choice(questions)
    return question["question"], question["options"], question["correct_option_index"]

def check_answer(selected_option_index, correct_option_index):
    """
    Checks if the selected answer is correct.
    
    :param selected_option_index: Index of the selected answer option.
    :param correct_option_index: Index of the correct answer option.
    :return: True if the selected option is correct, otherwise False.
    """
    return selected_option_index == correct_option_index

def update_score(user_id, points):
    """
    Updates the score for the given user.
    
    :param user_id: ID of the user whose score is to be updated.
    :param points: Points to add to the user's score.
    """
    if user_id in user_scores:
        user_scores[user_id] += points
    else:
        user_scores[user_id] = points

def get_score(user_id):
    """
    Retrieves the score for the given user.
    
    :param user_id: ID of the user whose score is to be retrieved.
    :return: The score of the user.
    """
    return user_scores.get(user_id, 0)

