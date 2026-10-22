import requests

# ------------------------ Extraction -------------------------- #

def fetch_flight_data():
    url = "https://opensky-network.org/api/states/all"    
    params = {
        "lamin": 36.9,
        "lamax": 42.2,
        "lomin": -9.6,
        "lomax": -6.1,
    }

    try:
        response = requests.get(url, params=params)

        response.raise_for_status() 

        return response.json()

    except Exception as e:
        print(f"Error: {e}")
        return None

# ------------------------ Extraction -------------------------- #

# ------------------------ Entrypoint -------------------------- #

if __name__ == "__main__":
    data = fetch_flight_data()
    if data:
        print("Successfully retrieved data!")
        print(f"Total vectors received: {len(data.get('states', []))}")
