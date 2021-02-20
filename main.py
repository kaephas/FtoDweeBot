import discord
import os

client = discord.Client()
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  prefix = '$dwee';
  if message.content.startswith(prefix):
    
    args = message.content[len(prefix):len(message.content)].split(' ')
    isNumber = 0
    try:
      val = int(args[1])
      isNumber = 1
    except ValueError:
      try:
        val = float(args[1])
        isNumber = 1
      except ValueError:
        print("not a number")
    if(isNumber):
      unit = ""
      if(len(args) > 2 and args[2] == '-c'):
        convert = (9/5) * val + 32
        unit = "Fahrenheit"
      else:
        convert = 5/9 * (val - 32)
        unit = "Celsius"
      await message.channel.send(str(round(convert, 2)) + " " + unit);
    else:
      await message.channel.send("Usage: $dwee # [-c (for C to F)]")

client.run(os.getenv('TOKEN'))