import requests
from bs4 import BeautifulSoup
import json

# URL della pagina meteo da cui estrarre i dati
WEATHERCLOUD_URL = "https://app.weathercloud.net/d2772110721#current"

def handler(event, context):
    try:
        response = requests.get(WEATHERCLOUD_URL)
        response.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        html_content = response.text
        
        # Analizza l'HTML con BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Funzione per estrarre i dati basandosi sull'ID
        def get_data(id):
            element = soup.find(id=id)
            return element.get_text(strip=True) if element else "N/A"

        # Estrai i dati desiderati
        data = {
            "temperature": get_data("d_2772110721_temp"),
            "humidity": get_data("d_2772110721_hum"),
            "pressure": get_data("d_2772110721_pres"),
            "wind_speed": get_data("d_2772110721_wind_avg"),
            "wind_direction": get_data("d_2772110721_wind_dir_text"),
            "rain_today": get_data("d_2772110721_rain_daily"),
            "dew_point": get_data("d_2772110721_dew_point"),
            "last_updated": get_data("d_2772110721_date_time")
        }
        
        # Restituisce i dati come JSON
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(data)
        }

    except Exception as e:
        error_message = {"error": f"Failed to retrieve data: {str(e)}"}
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(error_message)
        }
