import discord
import os
from keep_alive import keep_alive
from weather import getCityWeather, getDailyWeather

api_key = os.getenv('WEATHER_API')

client = discord.Client()
async def on_ready():
  await client.change_presence(activity=discord.Game('$dwee # (-c)'))
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  prefix = '$dwee'
  usage_string = "Usage: $dwee # (add -c for C to F) or $dwee {city}"
  if message.content.startswith(prefix):
    args = message.content[len(prefix):len(message.content)].split(' ')
    isNumber = 0
    isWeather = 0
    if(len(args) > 1):
      try:
        val = int(args[1])
        isNumber = 1
      except ValueError:
        try:
          val = float(args[1])
          isNumber = 1
        except ValueError:
          print("not a number")
          # weather
          city = ""
          if(len(args) == 2):
            city = args[1]
          elif(len(args) == 3):
            city = args[1] + " " + args[2]
          elif(len(args) > 3):
            for x in range(1, len(args) - 2):
              city += args[x] + " "
            city += args[len(args) - 1]
          else: # shouldn't get here
            await message.channel.send("An error has occurred.")
          weather = getCityWeather(city, api_key)
          if weather == 0:
            await message.channel.send("City " + city + " not found.")
          else:
            t = weather["main"]
            temp = t["temp"]
            celsius = temp - 273.15
            fahrenheit = celsius * (9/5) + 32
            z = weather["weather"]
            weather_description = z[0]["description"]
            await message.channel.send("Temperature: " + str(round(celsius, 2)) + "C" + " / " + str(round(fahrenheit, 2)) + "F - " + weather_description)

            coord = weather["coord"]
            lon = coord["lon"]
            lat = coord["lat"]
            daily = getDailyWeather(lat, lon, api_key)
            if daily != 0:
              tomorrow = daily["daily"]
              tomorrow = tomorrow[1]
              tomorrowTemp = tomorrow["temp"]
              maxTemp = tomorrowTemp["max"]
              tomorrowWeather = tomorrow["weather"]
              tomorrowWeather = tomorrowWeather[0]
              tomorrowDescription = tomorrowWeather["description"]
              tomorrowC = round(maxTemp - 273.15, 2)
              tomorrowF = str(round(tomorrowC * (9/5) + 32, 2)) + "F"
              tomorrowC = str(tomorrowC) + "C"
              tempString = tomorrowC + " / " + tomorrowF
              await message.channel.send("Tomorrow's forecast: " + tempString + " - " + tomorrowDescription)

            isWeather = 1     
      if(isNumber):
        unit = ""
        if(len(args) > 2 and args[2] == '-c'):
          convert = (9/5) * val + 32
          unit = "Fahrenheit"
        else:
          convert = 5/9 * (val - 32)
          unit = "Celsius"
        await message.channel.send(str(round(convert, 2)) + " " + unit);
      elif(not isWeather):
        await message.channel.send(usage_string)
    else:
      print("need to fix usage string")

keep_alive()
client.run(os.getenv('TOKEN'))