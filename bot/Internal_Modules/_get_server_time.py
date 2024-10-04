from datetime import datetime

def get_server_time():
    """Hämta den aktuella server-tiden och returnera i formatet HH:MM:SS (utan mikrosekunder)"""
    server_time = datetime.now()
    formatted_time = server_time.strftime('%H:%M:%S')
    return formatted_time
