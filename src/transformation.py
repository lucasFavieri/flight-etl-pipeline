import pandas as pd

# ------------------------ Trasformation -------------------------- #

def transform_flight_data(raw_data):
    if not raw_data or 'states' not in raw_data or not raw_data['states']:
        print("No data found")  
        return pd.DataFrame()

    states = raw_data["states"]

    # Scheme definition (column names)
    columns = [
        "icao24", "callsign", "origin_country", "time_position", 
        "last_contact", "longitude", "latitude", "baro_altitude", 
        "on_ground", "velocity", "true_track", "vertical_rate", 
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ]

    # Data Frame criation
    df = pd.DataFrame(states, columns=columns)

    if "time" in raw_data:
        df["extracted_at"] = pd.to_datetime(raw_data["time"], unit="s")

    df["callsign"] = df["callsign"].astype(str).str.strip()

    return df

# ------------------------ Trasformation -------------------------- #

# ------------------------ Entrypoint -------------------------- #

if __name__ == "__main__":
    # Imports the extration function
    from extraction import fetch_flight_data

    print("1. Extracting data from OpenSky...")
    raw_data = fetch_flight_data()

    print("2. Transforming data in a DataFrame...")
    df_flights = transform_flight_data(raw_data)

    if not df_flights.empty:
        print("\n--- Success! Flight table processed ---")

        showing_columns = ["callsign", "origin_country", "velocity", "latitude", "longitude", "extracted_at"]
        print(df_flights[showing_columns].head())
