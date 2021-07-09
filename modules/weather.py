import secret
import requests

def weather_request(): 

    api_key = secret.weather_api
    # Give city name 
    city_name = "90250"
        # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?appid={}&zip={}&units=imperial"
        # get method of requests module 
        # return response object 
    response = requests.get(base_url.format(api_key,city_name)).json()

    weather = {
            'city': city_name.split(',')[0], 
            'temperature': round(response['main']['temp']), 
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }
    return weather