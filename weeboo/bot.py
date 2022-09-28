import os
import re
import json
import requests
import discord
import random

BOT_TOKEN = os.environ['WEEBOO_TOKEN']
TENOR_TOKEN = os.environ['TENOR_TOKEN']

client = discord.Client()

def get_gif(query):
  r = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=discord&limit=10" 
    % (query, TENOR_TOKEN)
  )
  if r.status_code == 200:
    res = json.loads(r.content)
    return random.choice(res['results'])['media_formats']['tinygif']['url']
  return None

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  match = re.match('(.)(\w+)\s*(.*)', message.content)
  if match:
    pfx, cmd, arg = match.group(1, 2, 3)
    if pfx == '$':
      gif = get_gif(" ".join(["anime", cmd, arg]))
      if gif:
        await message.channel.send(gif)
    elif pfx == '&':
      gif = get_gif(" ".join([cmd, arg]))
      if gif:
        await message.channel.send(gif)

client.run(BOT_TOKEN)