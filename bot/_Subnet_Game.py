# This is _Subnet_Game.py

import ipaddress
import random

def generate_subnet_question():
    """
    Generates a random IP address and CIDR and asks a subnet-related question.
    Returns a tuple with the question and the correct answer.
    """
    # Create a random IP address
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    
    # Choose a random prefix length between /16 and /30
    prefix_length = random.randint(16, 30)
    
    # Create the network
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    
    # Choose a type of question
    question_type = random.choice(["network", "broadcast", "hosts"])

    if question_type == "network":
        question = f"What is the network address for {network}?"
        correct_answer = str(network.network_address)
    elif question_type == "broadcast":
        question = f"What is the broadcast address for {network}?"
        correct_answer = str(network.broadcast_address)
    else:  # hosts
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)  # Subtracts network and broadcast addresses
    
    return question, correct_answer

def check_answer(user_answer, correct_answer):
    """
    Compares the user's answer with the correct answer.
    Returns True if the answer is correct, otherwise False.
    """
    return user_answer.strip() == correct_answer
