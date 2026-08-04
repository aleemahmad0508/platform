import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read values from .env
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL")
def run_query(query: str):
    """
    Execute a PromQL query.
    """

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query},
    )

    return response.json()



def get_cpu_usage():
    query = 'sum(rate(container_cpu_usage_seconds_total[5m]))'
    return run_query(query)