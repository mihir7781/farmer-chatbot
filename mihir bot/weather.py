import requests
import json

def get_weather(city):
    api_key = "01981d11cbfdfb2b59e67e53988622f7"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # You can change this to 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

def format_weather_response(weather_data):
    if not weather_data:
        return "Sorry, I couldn't retrieve the weather information."

    main_info = weather_data['main']
    weather_info = weather_data['weather'][0]

    response = f"Weather in {weather_data['name']}: {weather_info['description']}\n"
    response += f"Temperature: {main_info['temp']}°C\n"
    response += f"Humidity: {main_info['humidity']}%\n"
    response += f"Wind Speed: {weather_data['wind']['speed']} m/s"

    return response

def weather_chatbot():
    print("Weather Chatbot: Hello! I can provide you with the current weather information.")
    
    while True:
        city = input("Enter the city name (or type 'exit' to quit): ")

        if city.lower() == 'exit':
            print("Weather Chatbot: Goodbye!")
            break

        weather_data = get_weather(city)

        if weather_data:
            response = format_weather_response(weather_data)
            print(f"Weather Chatbot: {response}")
        else:
            print("Weather Chatbot: Unable to fetch weather information. Please try again.")

weather_chatbot()