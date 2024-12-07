import requests
from requests.exceptions import RequestException


def check_health(url):
    try:
        response = requests.get(f"{url}/check/health/")
        response.raise_for_status()  
    except RequestException as err:
        print(f"Health check failed: {err}")
        exit(1) 

def check_db_connection(url):

    try:
        response = requests.get(f"{url}/check/db-connection/")
        response.raise_for_status() 
        if response.json().get('status') == 'healthy':
            print("Database connection is successful!")
        else:
            print("Database connection failed.")
            exit(1) 
    except RequestException as err:
        print(f"DB connection check failed: {err}")
        exit(1)  


if __name__ == "__main__":
    url = 'http://localhost:8000/api' 

    check_health(url)
    print("Health status ===ok===")

    check_db_connection(url)
    print("database connection ===ok===")
