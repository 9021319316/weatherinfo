import streamlit as st
import requests
import json
import datetime
from PIL import Image
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

# Function to encode an image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_hack(main_bg):
    bin_str = get_base64_of_bin_file(main_bg)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Specify the path to your background image
bg_image_path = "beach.png"
set_bg_hack(bg_image_path)

# Dates and Time
dt = datetime.datetime.now()
st.markdown(f"<h2 style='text-align: center; color: white; background-color:rgba(0, 0, 0, 0.5);'>{dt.strftime('%Y-%m-%d')}</h2>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center; color: white; background-color:rgba(0, 0, 0, 0.5);'>{dt.strftime('%I:%M %p')}</h2>", unsafe_allow_html=True)

# City Search
st.markdown("<style>input[type='text'] {font-size: 20px !important;}</style>", unsafe_allow_html=True)
city_name = st.text_input("Enter City name", "", max_chars=30)

# Function to fetch weather data
def fetch_weather_data(city):
    api_key = "dd1441b2810f9f56693732488d04cac6"
    api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}")
    return json.loads(api_request.content)

def fetch_forecast_data(city):
    api_key = "dd1441b2810f9f56693732488d04cac6"
    api_request = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}")
    return json.loads(api_request.content)

# Search Button
if st.button("Search"):
    if city_name:
        api = fetch_weather_data(city_name)
        forecast_api = fetch_forecast_data(city_name)
        
        # Extract weather details
        if 'main' in api:
            y = api['main']
            current_temperature = y['temp']
            humidity = y['humidity']
            temp_min = y['temp_min']
            temp_max = y['temp_max']

            x = api['coord']
            longitude = x['lon']
            latitude = x['lat']

            z = api['sys']
            country = z['country']
            state = z.get('state', '')  # State information might not be available
            city_name = api['name']

            weather = api['weather'][0]
            weather_icon = weather['icon']

            # Fetch weather icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))

            # Display data
            st.image(icon_image, width=100)

            # Transparent black box for information
            st.markdown(f"""
            <div style="background-color: rgba(0, 0, 0, 0.5); padding: 10px; border-radius: 10px; color: white;">
                <h3 style='text-align: center; color: white;'>City: {city_name}</h3>
                <h3 style='text-align: center; color: white;'>Country: {country}</h3>
                <h3 style='text-align: center; color: white;'>Longitude: {longitude}</h3>
                <h3 style='text-align: center; color: white;'>Latitude: {latitude}</h3>
                <h1 style='text-align: center; color: white;'>Temperature: {current_temperature} °C</h1>
                <h3 style='text-align: center; color: white;'>Humidity: {humidity}%</h3>
                <h3 style='text-align: center; color: white;'>Max Temp: {temp_max} °C</h3>
                <h3 style='text-align: center; color: white;'>Min Temp: {temp_min} °C</h3>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced graphical representation of the temperatures
            sns.set(style="whitegrid")

            fig, ax = plt.subplots()
            temps = [current_temperature, temp_min, temp_max]
            labels = ['Current Temp', 'Min Temp', 'Max Temp']

            # Set background color for the plot
            ax.set_facecolor((0, 0, 0, 0.5))  # Blackish transparent background for the plot area
        
            bar = ax.bar(labels, temps, color=['#ffffff99', '#ffffff99', '#ffffff99'], edgecolor='white', width=0.4)  # Slimmer and more transparent bars
            
            # Adding temperatures on top of bars
            for rect in bar:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., height,
                        f'{height}°C',
                        ha='center', va='bottom', color='black', fontweight='bold')

            ax.set_ylabel('Temperature (°C)', fontsize=12, color='black')
            ax.set_title(f'Temperature in {city_name}', fontsize=15, fontweight='bold', color='white')

            # Remove gridlines and spines
            ax.grid(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            st.pyplot(fig)

            # 4-day forecast
            if 'list' in forecast_api:
                st.markdown("<h2 style='text-align: center; color: white;'>6-Day Forecast</h2>", unsafe_allow_html=True)
                forecast_days = forecast_api['list'][:6]
                for day in forecast_days:
                    date_time = datetime.datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d %H:%M:%S')
                    temp = day['main']['temp']
                    weather_icon = day['weather'][0]['icon']
                    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
                    
                    # Fetch weather icon for forecast
                    icon_response = requests.get(icon_url)
                    icon_image = Image.open(BytesIO(icon_response.content))
                    
                    st.markdown(f"""
                    <div style="background-color: rgba(0, 0, 0, 0.5); padding: 10px; border-radius: 10px; margin-top: 10px; color: white;">
                        <h3 style='text-align: center; color: white;'>{date_time}</h3>
                        <img src="{icon_url}" style="display:block; margin-left:auto; margin-right:auto; width:50px; height:50px;">
                        <h3 style='text-align: center; color: white;'>Temp: {temp} °C</h3>
                    </div>
                    """, unsafe_allow_html=True)

        else:
            st.error("City not found. Please enter a valid city name.")
