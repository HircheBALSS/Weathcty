from django.shortcuts import render
import urllib.request
import json

def home(request):
    if 'city' in request.GET:
        city = request.GET.get('city')
        source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' + 
                                        city + '&units=metric&appid=da9408e8d19903267820876efa42cdde').read()
        json_data = json.loads(source)
        

        res_json = {
            "city_name": str(json_data['name']),
            "Code_country": str(json_data['sys']['country']),
            "coordonate": str(json_data['coord']['lat']) + ', ' + str(json_data['coord']['lon']),
            "temp": str(json_data['main'] ['temp']) + ' °C',
            "pressure": str(json_data['main'] ['pressure']),
            "humidity": str(json_data['main'] ['humidity']),
            "description": str(json_data['weather'][0]['description']),
            "main": str(json_data ['weather'][0]['main']),
            "icon": str(json_data ['weather'][0]['icon']),
        }

        print(res_json)

    else:
        res_json = {}

    return render(request, 'core/accueil.html', {'res_json': res_json})
