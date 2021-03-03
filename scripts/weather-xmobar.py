#!/usr/bin/python
# my script for getting weather stats with the Nerd Font icons
# Data is pulled from the wttr.in in the JSON format

# import sys
import requests
import json
import datetime

# mapping standard wind rose into arrows
wind_directions = {
    "S": "",
    "N": "",
    "E": "",
    "W": "",
    "NNW": "",
    "NW": "",
    "WNW": "",
    "WSW": "",
    "SW": "",
    "SSW": "",
    "SSE": "",
    "SE": "",
    "ESE": "",
    "NNE": "",
    "NE": "",
    "ENE": ""
}

# mapping of weather codes into day icons 
# I use icons from the NerdFont
weather_icons_night = {
    # Sunny
    "113": "",
    # Partly Cloudy
    "116": " ",
    # Cloudy
    "119": "摒",
    # Very Cloudy
    "122": " ",
    # Fog
    "143": " ",
    "248": " ",
    "260": " ",
    # Light Showers
    "176": " ",
    "263": " ",
    # Light Sleet Showers
    "179": " ",
    "362": " ",
    "365": " ",
    "374": " ",
    # Light Sleet
    "182": " ",
    "185": " ",
    "281": " ",
    "284": " ",
    "311": " ",
    "314": " ",
    "317": " ",
    "350": " ",
    "377": " ",
    # Thundery Showers
    "200": " ",
    # Light Snow
    "227": " ",
    "320": " ",
    # Heavy Snow
    "230": " ",
    # Light rain
    "266": " ",
    "293": " ",
    "296": " ",
    # Heavy Showers
    "299": " ",
    "305": " ",
    "356": " ",
    # Heavy Rain
    "302": " ",
    "308": " ",
    "359": " ",
    # Light Snow Showers
    "323": "ﭽ ",
    "326": "ﭽ ",
    "368": "ﭽ ",
    # Heavy Snow Showers
    "335": "ﭽ ",
    "395": "ﭽ ",
    "371": "ﭽ ",
    # Heavy Snow
    "329": "流",
    "332": "流",
    "338": "流",
    # Light showers
    "353": " ",
    # Thundery Showers
    "386": " ",
    "389": " ",
    # Thundery Snow Showers
    "392": " "
}

weather_icons_day = {
    # Sunny
    "113": " ",
    # Partly Cloudy
    "116": "杖",
    # Cloudy
    "119": "摒",
    # Very Cloudy
    "122": " ",
    # Fog
    "143": " ",
    "248": " ",
    "260": " ",
    # Light Showers
    "176": " ",
    "263": " ",
    # Light Sleet Showers
    "179": " ",
    "362": " ",
    "365": " ",
    "374": " ",
    # Light Sleet
    "182": " ",
    "185": " ",
    "281": " ",
    "284": " ",
    "311": " ",
    "314": " ",
    "317": " ",
    "350": " ",
    "377": " ",
    # Thundery Showers
    "200": "  ",
    # Light Snow
    "227": " ",
    "320": " ",
    # Heavy Snow
    "230": " ",
    # Light rain
    "266": " ",
    "293": " ",
    "296": " ",
    # Heavy Showers
    "299": " ",
    "305": " ",
    "356": " ",
    # Heavy Rain
    "302": " ",
    "308": " ",
    "359": " ",
    # Light Show Showers
    "323": "ﭽ ",
    "326": "ﭽ ",
    "368": "ﭽ ",
    # Heavy Snow Showers
    "335": "ﭽ ",
    "395": "ﭽ ",
    "371": "ﭽ ",
    # Heavy Snow
    "329": "流",
    "332": "流",
    "338": "流",
    # Light showers
    "353": " ",
    # Thundery Showers
    "386": " ",
    "389": " ",
    # Thundery Snow Showers
    "392": " ",
}

# Function to convert %I:%M AM/PM format of time into 24 hours
def convert24(str1) -> str: # input format must be %I:%M AM/PM (no seconds)
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-3]
    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-3]
    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:5]

# Function to return night or day icon for a given weather code
# As input function takes map which must contain values for:
# 'sunrise', 'sunset' and 'weatherCode'
def day_or_night(weather_map) -> str:
    current_time_int = int(datetime.datetime.now().strftime("%H%M"))
    sunrise_int = int(weather_map['sunrise'][:2] + weather_map['sunrise'][3:5])
    sunset_int = int(weather_map['sunset'][:2] + weather_map['sunset'][3:5])
    if current_time_int < sunrise_int:
        return 'night'
    elif current_time_int < sunset_int:
        return 'day'
    else:
        return 'unknown'

def return_icon(weather_map) -> str:
    days_time = day_or_night(weather_map)
    if days_time == 'night':
        return weather_icons_night.get(weather_map['weatherCode'],' ')
    elif days_time == 'day':
        return weather_icons_day.get(weather_map['weatherCode'],' ')
    else:
        return weather_icons_day.get(weather_map['weatherCode'],' ')

# function to wrap into the standard xmobar front color notation
def wrap_xmobar_color(color: str, data: str) -> str:
    return '<fc=' + color + '>' + data + '</fc>'

# function to assemble weather reporting string for xmobar
def make_xmobar_weather_string(weather_map) -> str:
    days_time = day_or_night(weather_map)
    report_string = ''
    if days_time == 'day':
        report_string += wrap_xmobar_color('#FFFF00',return_icon(weather_map)) + ' '
    elif days_time == 'night':
        report_string += wrap_xmobar_color('#1E90FF',return_icon(weather_map)) + ' '
    else:
        report_string += wrap_xmobar_color('white',return_icon(weather_map)) + ' '
    report_string += wrap_xmobar_color('green',weather_map['temp_C']) + '('
    report_string += wrap_xmobar_color('green',weather_map['FeelsLikeC']) + ')°C '
    report_string += wrap_xmobar_color('white',wind_directions.get(weather_map["winddir16Point"],'')) + ':'
    report_string += wrap_xmobar_color('#FF1493',str(int(weather_map['windspeedKmph']) * 10 // 36)) + 'm/s '
    report_string += wrap_xmobar_color('cyan','' + weather_map['humidity'] + '%')
    return report_string

def main():
    weather_URL = 'http://wttr.in/'
    city = 'Bonn'
    weather_report = ""
    # Here I define arrays with the data I collect
    current_weather_temperature =  ['temp_C','FeelsLikeC']
    current_weather_conditions =  ['windspeedKmph','humidity','weatherCode','winddir16Point']
    current_weather_map = {}
    # in the case of errors (either connectivity or JSON parsing)
    # I just put "N/A" message in a yellow color
    try:
        response = requests.get(weather_URL + city + '\?format=j1').json()
        for temperature in current_weather_temperature:
            if '-' in response['current_condition'][0][temperature]:
                current_weather_map[temperature] = response['current_condition'][0][temperature]
            else:
                current_weather_map[temperature] = '+' + response['current_condition'][0][temperature]
        for condition in current_weather_conditions:
            current_weather_map[condition] = response['current_condition'][0][condition]
        current_weather_map['sunrise'] = convert24(response['weather'][0]['astronomy'][0]['sunrise'])
        current_weather_map['sunset'] = convert24(response['weather'][0]['astronomy'][0]['sunset'])
        weather_report = make_xmobar_weather_string(current_weather_map)
    except requests.RequestException:
        weather_report = wrap_xmobar_color("yellow","____N/A____")
    except json.decoder.JSONDecodeError:
        weather_report = wrap_xmobar_color("yellow","____N/A____")
    print(weather_report)

main()
