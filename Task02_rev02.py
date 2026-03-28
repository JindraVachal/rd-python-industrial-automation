import keyboard
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

TOMORROW_API_KEY = "xZBVbDK0bCu4IKkbEAY4PgQuK55cTUst" 

def get_location():
    try:
        # Zjištění veřejné IP adresy
        ip = requests.get('https://api.ipify.org').text
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data["lat"], data["lon"]
        
        raise Exception("Nepodařilo se zaměřit IP")
    except Exception as e: 
        print(f"Chyba lokace: {e}")
        mesto = input("Zadej název svého města (anglicky, např. Prague): ")
        return mesto

def get_weather_to_csv(location):
    url = "https://api.tomorrow.io/v4/weather/forecast"
    file_name = "pocasi_zitra.csv"
    
    zitra = datetime.now() + timedelta(days=1)
    start_time = zitra.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    end_time = zitra.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"

    loc_param = f"{location[0]},{location[1]}" if isinstance(location, tuple) else location

    params = {
        "location": loc_param,
        "fields": ["temperature", "windSpeed", "humidity"],
        "units": "metric",
        "timesteps": "1h",
        "apikey": TOMORROW_API_KEY,
        "startTime": start_time,
        "endTime": end_time
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            intervals = data['timelines']['hourly']
            
            df = pd.DataFrame([{
                "cas": entry['time'],
                "teplota": entry['values']['temperature'],
                "vitr": entry['values']['windSpeed'],
                "vlhkost": entry['values']['humidity']
            } for entry in intervals])
            
            df.to_csv(file_name, index=False)
            return file_name, start_time[:10]
        else:
            print(f"Chyba API ({response.status_code}): {response.text}")
            return None, None
    except Exception as e:
        print(f"Chyba při stahování dat: {e}")
        return None, None

def plot_weather(file_name, datum):
    df = pd.read_csv(file_name)
    df['cas'] = pd.to_datetime(df['cas'])
    
    fig = px.line(df, x="cas", y="teplota", 
                 title=f"Předpověď teploty na {datum}",
                 labels={'teplota': 'Teplota (°C)', 'cas': 'Čas (hodiny)'},
    
                 markers=True)
    print("Zmáčkni 0 = Print na web, Zmáčkni 1 = Print do souboru graf.html")
    while True:
        if keyboard.is_pressed('0'):
            print("Print na web")
            fig.show()
            break  # Ukončí cyklus po zobrazení

        elif keyboard.is_pressed('1'):
            print("Print do souboru graf.html")
            fig.write_html(r"E:\DATA\Python\r_d\Vizualizace dat_08032026\graf.html")
            break  # Ukončí cyklus po uložení
    
    #fig.show()

def main():
    print("Zjišťuji polohu...")
    location = get_location()
    
    if location:
        print(f"Lokalita nalezena. Stahuji data pro: {location}")
        csv_file, datum = get_weather_to_csv(location)
        if csv_file:
            plot_weather(csv_file, datum)
            print(f"Hotovo! Data uložena v {csv_file}")

if __name__ == "__main__":
    main()