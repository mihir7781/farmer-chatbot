import tkinter as tk
from tkinter import scrolledtext

import wikipedia
import requests
import spacy
from PIL import Image, ImageTk

nlp = spacy.load("en_core_web_sm/en_core_web_sm-3.7.1")

def extract_city_names(sentence):
    doc = nlp(sentence)
    city_names = []

    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE stands for geopolitical entity (e.g., city)
            city_names.append(ent.text)
    print(city_names)
    return city_names

#@register_call("whoIs")
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

#@register_call("getWeather")
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
        try:
            city = extract_city_names(user_input)
            return get_weather(None, city[0].lower())
        except IndexError as e:
            return "No city of this name exists"
    else:
        return who_is(None, user_input)

def send_message():
    user_input = user_entry.get()
    if user_input.lower() == "exit":
        root.destroy()
    else:
        response = chatbot_main(user_input)
        chat_box.insert(tk.END, f"You: {user_input}\n")
        res=""
        flag=0
        for i in response:
            if i==".":
                flag+=1
            res=res+i
            if(flag==3):
                break
        chat_box.insert(tk.END, f"Chatbot: {res}\n")
        user_entry.delete(0, tk.END)

def clear_chat():
    chat_box.delete(1.0, tk.END)

root = tk.Tk()
root.configure(bg='#3498db')
root.title("Chatbot GUI")
#Image.ANTIALIAS
# Load and resize the logo image
logo_image = Image.open("dsu.png")
logo_image = logo_image.resize((90, 90))
tk_logo_image = ImageTk.PhotoImage(logo_image)

# Add logo and labels
logo_label = tk.Label(root, image=tk_logo_image, bg='#3498db')
logo_label.pack(padx=10, pady=5, anchor=tk.CENTER)

credits_label = tk.Label(root, text="Dayananda Sagar University, Bengaluru", font=("Helvetica", 25), fg='white', bg='#3498db')
credits_label.pack(side=tk.TOP, pady=5)

credits_label1 = tk.Label(root, text="Dept. of Computer Science and Engineering", font=("Helvetica", 15), fg='white', bg='#3498db')
credits_label1.pack(side=tk.TOP, pady=5)

# Chat box and entry
chat_box = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
chat_box.pack(padx=10, pady=5)

user_entry = tk.Entry(root, width=60)
user_entry.pack(padx=10, pady=5)

# Buttons
send_button = tk.Button(root, text="Send", command=send_message, bg='#2ecc71', fg='white', width=20)
send_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_chat, bg='#e74c3c', fg='white', width=20)
clear_button.pack(pady=3)

credits_label2 = tk.Label(root, text="Designed by Mihir, Ishita, Karishma, Niyati", font=("Helvetica", 16), fg='white', bg='#3498db')
credits_label2.pack(side=tk.BOTTOM, pady=0)

root.mainloop()