import ipaddress
import random

def generate_subnet_question():
    """
    Genererar en slumpmässig IP-adress och CIDR och ställer en fråga om subnät.
    Returnerar en tuple med frågan och rätt svar.
    """
    # Skapa en slumpmässig IP-adress
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    
    # Välj en slumpmässig prefixlängd mellan /16 och /30
    prefix_length = random.randint(16, 30)
    
    # Skapa nätverket
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    
    # Välj en typ av fråga
    question_type = random.choice(["network", "broadcast", "hosts"])

    if question_type == "network":
        question = f"Vad är nätverksadressen för {network}?"
        correct_answer = str(network.network_address)
    elif question_type == "broadcast":
        question = f"Vad är broadcast-adressen för {network}?"
        correct_answer = str(network.broadcast_address)
    else:  # hosts
        question = f"Hur många värdar kan finnas i subnätet {network}?"
        correct_answer = str(network.num_addresses - 2)  # Subtraherar nätverks- och broadcastadresser
    
    return question, correct_answer

def check_answer(user_answer, correct_answer):
    """
    Jämför användarens svar med det korrekta svaret.
    Returnerar True om svaret är rätt, annars False.
    """
    return user_answer.strip() == correct_answer
