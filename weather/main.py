from tkinter import *
from tkinter import ttk
import requests
import json

window = Tk()
API_KEY = "your_api_key_here"  # Replace with your actual API key from "https://www.weatherapi.com/api-explorer.aspx"

notebook = ttk.Notebook(window)
window.geometry("500x500") 
window.title("Weather")
tab1 = Frame(notebook)
notebook.add(tab1, text="Current Weather")
notebook.pack(expand=True, fill="both")

cities = ["Toronto", "New York", "London", "Paris", "Tokyo", "Ontario"]
cb_city = ttk.Combobox(tab1, values=cities, state="readonly") 
cb_city.set("Toronto")  # Set the default value
cb_city.pack(pady=10)

label = Label(tab1, text="Select a city to get the current weather", font=("Arial", 14))
label.pack(pady=10)

def get_weather():
    cb_city_value = cb_city.get()
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cb_city_value}&aqi=no"
    headers = {"Authorization": "Bearer " + API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        weather_info = f"City: {data['location']['name']}\nTemperature: {data['current']['temp_c']}°C\nCondition: {data['current']['condition']['text']}"
        label_weather.config(text=weather_info)

    else:   
        label_error = Label(tab1, text="Failed to retrieve weather data", font=("Arial", 14), fg="red")
        label_error.pack(pady=10)

label_weather = Label(tab1, text="", font=("Arial", 14))
label_weather.pack(pady=10)

Button(tab1, text="Get Weather", command=get_weather).pack(pady=10)

window.mainloop()
