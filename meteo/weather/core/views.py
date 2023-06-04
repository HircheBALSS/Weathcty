from django.shortcuts import render
import requests
import datetime


def home(request):
    API_KEY = 'f13c2d9b4e28d8257a753f26243b4a84'
    meteo_url = f"https://api.openweathermap.org/data/2.5/weather?q={{}}&appid={API_KEY}"
    forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={{}}&lon={{}}&exclude=current,minutely,hourly,alerts&appid={API_KEY}"

    if request.method == "POST":
        city = request.POST['city']

        meteo_data, forecasts = fetch_meteo_and_forecast(city, meteo_url, forecast_url)

        # print("Meteo Data:")
        # print(meteo_data)
        # print("Forecasts:")
        # print(forecasts)

        context = {
            "meteo_data": meteo_data,
            "forecasts": forecasts,
        }

        return render(request, 'core/accueil.html', context)
    else:
        return render(request, 'core/accueil.html')

def fetch_meteo_and_forecast(city, meteo_url, forecast_url):
    meteo_response = requests.get(meteo_url.format(city)).json()
    lat, lon = meteo_response['coord']['lat'], meteo_response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon)).json()

    meteo_data = {
        "city": city,
        "temperature": round(meteo_response['main']['temp'] - 273.15, 2),
        "description": meteo_response['weather'][0]['description'],
        "icon": meteo_response['weather'][0]['icon'],
    }

    forecasts = []
    for data_forecast in forecast_response.get('daily', [])[:3]:
     forecasts.append({
            "day": datetime.datetime.fromtimestamp(data_forecast['dt']).strftime("%A"),
            "min_temp": round(data_forecast['temp']['min'] - 273.15, 2),
            "max_temp": round(data_forecast['temp']['max'] - 273.15, 2),
            "description": data_forecast['weather'][0]['description'],
            "icon": data_forecast['weather'][0]['icon'],
        })

    return meteo_data, forecasts