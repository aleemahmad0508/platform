import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read values from .env
ALERTMANAGER_URL = os.getenv("ALERTMANAGER_URL")
def get_alerts():
    """
    Return all active alerts.
    """

    response = requests.get(
        f"{ALERTMANAGER_URL}/api/v2/alerts"
    )

    return response.json()