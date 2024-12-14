from datetime import datetime, timezone, timedelta
import requests

def fetch_and_save_csv():
    # Generate current datetime and 12 hours from now in ISO format for URL parameters
    start_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    end_time = (datetime.now(timezone.utc) + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    # Elering API URL with dynamically inserted start and end times
    ELERING_CSV_URL = (
        f"https://dashboard.elering.ee/api/nps/price/csv?start={start_time}"
        f"&end={end_time}&fields=ee"
    )
    
    try:
        # Fetch the CSV data from Elering API
        response = requests.get(ELERING_CSV_URL)
        response.raise_for_status()
        
        # Write the content to "hinnaandmed.csv"
        with open("~/pildiraam/hinnaandmed.csv", mode="wb") as file:
            file.write(response.content)
        
        with open("~/pildiraam/hindadevärskendamiseaeg.txt", mode="w", encoding="utf-8") as file:
            file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CSV from Elering API: {e}")

# Call the function
fetch_and_save_csv()
