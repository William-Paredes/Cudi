#!/usr/bin/env python3

import argparse
import pathlib
import sys
import datetime
import requests

from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
from inky.auto import auto

weather_api = ''
api_key = weather_api
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

temp = str(weather['temperature']) + '°'
inky = auto(ask_user=True, verbose=True)
inky.set_border(inky.WHITE)

font = ImageFont.truetype(FredokaOne, 36)

img = Image.new("P", (inky.WIDTH, inky.HEIGHT))

draw = ImageDraw.Draw(img)

now = datetime.datetime.now()
message = now.strftime("%B %d\n%A")
_, _, w, h = font.getbbox(message)
x = (inky.width / 2) - (w / 2)
y = (inky.height / 2) - (h / 2)
# 600X448
x1 = x-100
x2 = x+300
y1 = y-175
y2 = y+165

draw.rectangle([x1,y1,x2,y2], inky.WHITE)

draw.multiline_text((x, y1+25), message, inky.BLACK, font, None, 20)
draw.multiline_text((x, y1+200), temp, inky.BLACK, font, None, 20)

#icon
icon_image = Image.open('01d.png').convert("RGBA")
icon_image = icon_image.resize((100, 100))
img.paste(icon_image, (x, y2-100), icon_image)

try:
    inky.set_image(img)
except TypeError:
    inky.set_image(img)

inky.show()