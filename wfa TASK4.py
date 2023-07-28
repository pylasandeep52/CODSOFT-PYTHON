import requests
import tkinter as tk
from tkinter import messagebox

def marquee():
    global marquee_offset, color_index
    canvas.coords(text_id, marquee_offset, 10)
    marquee_offset -= 1
    if marquee_offset <= -marquee_text_width:
        marquee_offset = window_width
    canvas.itemconfig(text_id, fill=colors[color_index])  # Change text color
    color_index = (color_index + 1) % len(colors)  # Move to the next color
    canvas.after(3, marquee)  # Update every 3 milliseconds


# Function to fetch weather data from the API
def get_weather():
    api_key = "ec6265cdf71845f11f3562c11ce376ad"  # Replace with your actual API key
    city = city_entry.get()
    zip_code = zip_entry.get()

    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    elif zip_code:
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}&units=metric"
    else:
        messagebox.showwarning("Weather Forecast", "Please enter either the city name or the zip code.")
        return

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            # Extract relevant weather information
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]

            # Fetch pollution data
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={data['coord']['lat']}&lon={data['coord']['lon']}&appid={api_key}"
            pollution_response = requests.get(pollution_url)
            pollution_data = pollution_response.json()
            air_quality = pollution_data["list"][0]["components"]["pm2_5"]

            # Fetch rain forecast data
            rain_forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            rain_forecast_response = requests.get(rain_forecast_url)
            rain_forecast_data = rain_forecast_response.json()
            if "list" in rain_forecast_data:
                rain_time = None
                for forecast in rain_forecast_data["list"]:
                    if "rain" in forecast:
                        rain_time = forecast["dt_txt"]
                        break

            # Display the weather information to the user
            info_message = f"Weather in {city}:\n\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {description.capitalize()}\nAir Quality (PM2.5): {air_quality} μg/m³"
            if rain_time:
                info_message += f"\n\nRain Forecast: Rain is expected at {rain_time}"
            messagebox.showinfo("Weather Forecast", info_message)
        else:
            messagebox.showwarning("Weather Forecast", f"City not found: {city}")

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "An error occurred. Please check your internet connection.")

# Initialize the main window
app = tk.Tk()
app.title("Weather Forecast Application")
app.geometry("500x300")

marquee_text = "Weather Forecast application"
canvas = tk.Canvas(app, width=1500, height=28)
canvas.pack(pady=15)

# Draw the marquee text on the canvas
text_id = canvas.create_text(1000,3,text=marquee_text, font=('Helvetica', 12), anchor='e', fill='black')

# Measure the width of the marquee text to know when to wrap around
marquee_text_width = canvas.bbox(text_id)[2] - canvas.bbox(text_id)[0]

window_width = 1000
marquee_offset = window_width

# List of colors to cycle through
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown' , '#ffc3a0' , '#6dd5ed' , '#753a88']
color_index = 0

marquee()


# Create labels and entry fields
city_label = tk.Label(app, text="City:")
city_label.pack(pady=5)

city_entry = tk.Entry(app, width=20)
city_entry.pack(pady=5)

zip_label = tk.Label(app, text="Zip Code (Pin Code):")
zip_label.pack(pady=5)

zip_entry = tk.Entry(app, width=20)
zip_entry.pack(pady=5)

# Create the "Get Weather" button
get_weather_button = tk.Button(app, text="Get Weather", command=get_weather, bg='#ffc3a0', fg='#141e30')
get_weather_button.pack(pady=10)

app.mainloop()
