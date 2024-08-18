# _Games.py

import ipaddress
import random
import asyncio

# Global variables to keep track of current game state
current_question = None
correct_answer = None
game_type = None
game_task = None

async def start_game(ctx, chosen_game):
    global current_question, correct_answer, game_type, game_task

    if game_task and not game_task.done():
        await ctx.send("A game is already in progress. Please use `./stop_game` to stop it first.")
        return

    game_type = chosen_game
    current_question, correct_answer = generate_question(chosen_game)
    
    intro_message = (
        "Welcome to the Network Game!\n\n"
        "Here's how to play:\n"
        "1. You will be asked a question related to IP subnets or network concepts.\n"
        "2. Please reply with your answer directly in this chat.\n"
        "3. The bot will check if your answer is correct and inform you accordingly.\n\n"
        "Good luck, and let's get started!\n\n"
        f"**Question:** {current_question}"
    )
    await ctx.send(intro_message)
    
    # Start the game timer
    game_task = asyncio.create_task(run_game_timer(ctx, 5 * 60))  # 5 minutes in seconds

def generate_question(game_type):
    """
    Generates a random question based on the chosen game type.
    """
    if game_type == 'subnet':
        return generate_subnet_question()
    elif game_type == 'network':
        return generate_network_question()
    else:
        raise ValueError("Invalid game type")

def generate_subnet_question():
    """
    Generates a random IP address and CIDR and asks a subnet-related question.
    Returns a tuple with the question and the correct answer.
    """
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    prefix_length = random.randint(16, 30)
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    question_type = random.choice(["network", "broadcast", "hosts"])

    if question_type == "network":
        question = f"What is the network address for {network}?"
        correct_answer = str(network.network_address)
    elif question_type == "broadcast":
        question = f"What is the broadcast address for {network}?"
        correct_answer = str(network.broadcast_address)
    else:
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)
    
    return question, correct_answer

def generate_network_question():
    """
    Generates a random network-related question (e.g., BGP configuration).
    """
    questions = [
        {"question": "What is the default administrative distance for eBGP?", "correct_answer": "20"},
        {"question": "What command shows the BGP neighbors?", "correct_answer": "show ip bgp summary"},
        {"question": "Which protocol is used for routing between different ASes?", "correct_answer": "eBGP"},
        {"question": "What does VLAN stand for?", "correct_answer": "Virtual Local Area Network"},
        {"question": "Which protocol is used for secure communication over the internet?", "correct_answer": "HTTPS"},
        {"question": "What is the purpose of the DHCP protocol?", "correct_answer": "Assign IP addresses dynamically"},
        {"question": "Which layer of the OSI model does a switch operate at?", "correct_answer": "Layer 2"},
        {"question": "What is the main function of the ARP protocol?", "correct_answer": "Resolve IP addresses to MAC addresses"},
        {"question": "What does the acronym OSPF stand for?", "correct_answer": "Open Shortest Path First"},
        {"question": "Which layer of the OSI model does the IP protocol operate on?", "correct_answer": "Layer 3"},
        {"question": "In which protocol is the TTL (Time To Live) field used?", "correct_answer": "IP"},
        {"question": "What does NAT stand for in networking?", "correct_answer": "Network Address Translation"},
        {"question": "Which protocol is used for encrypting data in a VPN?", "correct_answer": "IPsec"},
        {"question": "What is the default administrative distance of OSPF?", "correct_answer": "110"},
        {"question": "What is the purpose of a VLAN?", "correct_answer": "To segment broadcast domains"},
        {"question": "Which type of DNS record is used to map domain names to IP addresses?", "correct_answer": "A"},
        {"question": "What does BGP stand for?", "correct_answer": "Border Gateway Protocol"},
        {"question": "What is the primary function of the ARP protocol?", "correct_answer": "Translate IP addresses to MAC addresses"},
        {"question": "In the context of network security, what does IDS stand for?", "correct_answer": "Intrusion Detection System"},
        {"question": "Which command is used to view the routing table on a Cisco router?", "correct_answer": "show ip route"},
        {"question": "Which layer of the OSI model does a hub operate on?", "correct_answer": "Layer 1"},
        {"question": "What is the maximum length of a segment in Ethernet (in meters)?", "correct_answer": "100 meters"},
        {"question": "Which of the following is a routing protocol that uses distance-vector algorithms?", "correct_answer": "RIP"},
        {"question": "What type of network device connects multiple networks and routes packets between them?", "correct_answer": "Router"},
        {"question": "What does the acronym VPN stand for?", "correct_answer": "Virtual Private Network"},
        {"question": "Which of the following protocols is used for network time synchronization?", "correct_answer": "NTP"},
        {"question": "What is the purpose of the STP protocol?", "correct_answer": "Prevent loops in a network"},
        {"question": "Which command is used to display the current configuration on a Cisco device?", "correct_answer": "show running-config"},
        {"question": "What is the purpose of a subnet mask?", "correct_answer": "To define the network and host portions of an IP address"},
        {"question": "What type of cable is used for connecting devices in a LAN over short distances?", "correct_answer": "Twisted pair"},
        {"question": "What is the main difference between TCP and UDP?", "correct_answer": "TCP is connection-oriented, while UDP is connectionless"},
        {"question": "Which protocol uses port 80 by default?", "correct_answer": "HTTP"},
        {"question": "What does the acronym DHCP stand for?", "correct_answer": "Dynamic Host Configuration Protocol"},
        {"question": "In a Cisco router, which command is used to configure an IP address on an interface?", "correct_answer": "ip address [address] [mask]"},
        {"question": "What is the purpose of the DNS protocol?", "correct_answer": "Translate domain names to IP addresses"},
        {"question": "Which of the following is a class of IP address reserved for multicast communication?", "correct_answer": "Class D"},
        {"question": "What is the purpose of a firewall in network security?", "correct_answer": "To control incoming and outgoing network traffic"},
        {"question": "Which protocol provides dynamic IP address allocation?", "correct_answer": "DHCP"},
        {"question": "What does the acronym VPN stand for?", "correct_answer": "Virtual Private Network"},
        {"question": "What layer of the OSI model does SSL/TLS operate on?", "correct_answer": "Layer 4"},
        {"question": "Which command is used to verify the connectivity between two devices on a network?", "correct_answer": "ping"},
        {"question": "What does the acronym QoS stand for in networking?", "correct_answer": "Quality of Service"},
        {"question": "What is the default port number for HTTPS?", "correct_answer": "443"},
        {"question": "Which device operates at Layer 2 of the OSI model?", "correct_answer": "Switch"},
        {"question": "What is the maximum length of a cable segment in a 10BaseT Ethernet network?", "correct_answer": "100 meters"},
        {"question": "Which of the following protocols is used for network management?", "correct_answer": "SNMP"},
        {"question": "What does the acronym VPN stand for?", "correct_answer": "Virtual Private Network"},
        {"question": "Which of the following is used to provide secure remote access to a network?", "correct_answer": "VPN"},
        {"question": "What does the acronym RIP stand for?", "correct_answer": "Routing Information Protocol"},
        {"question": "In which protocol is the SYN flag used?", "correct_answer": "TCP"},
        {"question": "Which command is used to view the interface status on a Cisco device?", "correct_answer": "show interfaces"},
        {"question": "Which protocol is used to automatically assign IP addresses to devices on a network?", "correct_answer": "DHCP"},
        {"question": "What is the function of the ICMP protocol?", "correct_answer": "Error reporting and diagnostic functions"},
        {"question": "What does the acronym EIGRP stand for?", "correct_answer": "Enhanced Interior Gateway Routing Protocol"},
        {"question": "Which layer of the OSI model is responsible for end-to-end communication and error recovery?", "correct_answer": "Layer 4"},
        {"question": "Which command is used to reload a Cisco device?", "correct_answer": "reload"},
        {"question": "What does the acronym AAA stand for in network security?", "correct_answer": "Authentication, Authorization, and Accounting"},
        {"question": "What is the primary purpose of a proxy server?", "correct_answer": "To act as an intermediary between clients and servers"},
        {"question": "Which protocol is used to secure communication between a web server and a browser?", "correct_answer": "HTTPS"},
        {"question": "What does the acronym MPLS stand for?", "correct_answer": "Multi-Protocol Label Switching"}
    ]
    question = random.choice(questions)
    return question["question"], question["correct_answer"]

async def run_game_timer(ctx, duration):
    """
    Runs a timer for the specified duration and stops the game when time is up.
    """
    await asyncio.sleep(duration)
    if game_task and not game_task.done():
        await ctx.send("Time is up! The game has ended.")
        reset_game()

def reset_game():
    global current_question, correct_answer, game_type, game_task
    current_question = None
    correct_answer = None
    game_type = None
    if game_task and not game_task.done():
        game_task.cancel()
        game_task = None

def check_answer(user_answer):
    """
    Compares the user's answer with the correct answer.
    Returns True if the answer is correct, otherwise False.
    """
    return user_answer.strip() == correct_answer
