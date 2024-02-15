from chatbot import Chat, register_call
import wikipedia
import requests
import spacy

nlp = spacy.load("en_core_web_sm/en_core_web_sm-3.7.1")

def extract_city_names(sentence):
    doc = nlp(sentence)
    city_names = []

    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE stands for geopolitical entity (e.g., city)
            city_names.append(ent.text)
    print(city_names)
    return city_names

@register_call("whoIs")
def who_is(session, query):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about " + query

@register_call("getWeather")
def get_weather(session, city):
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
        return format_weather_response(weather_data)
    else:
        return "Unable to fetch weather information for " + city

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

def chatbot_main(user_input):
    # Check if the user's input contains the word "weather"
    if 'weather' in user_input.lower():
        city = extract_city_names(user_input)
        return get_weather(None, city[0].lower())
    else:
        return who_is(None, user_input)

# Example usage
exit=1
while(exit):
    user_input = input("You: ")
    if(user_input=="exit"):
        break
    response = chatbot_main(user_input)
    print("Chatbot:", response)
