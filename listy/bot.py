# token: MTA1MTM1MTAzMDgyNDE5NDIwOQ.GOvVSR.EJVF6NUdDeK0a2uXHwh_ImVgjVHSOqRkXo5WhE

import os
import re
import json
import requests
import discord
import random

BOT_TOKEN = "MTA1MTM1MTAzMDgyNDE5NDIwOQ.GOvVSR.EJVF6NUdDeK0a2uXHwh_ImVgjVHSOqRkXo5WhE"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# A dictionary to store the lists of items for each channel
channel_lists = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message starts with "#add"
    if message.content.startswith('#add'):
        # Get the item from the message
        item = message.content[5:]

        # Get the list of items for the current channel
        channel = message.channel
        items = channel_lists.get(channel, [])

        # Add the item to the list
        items.append(item)
        channel_lists[channel] = items

        await message.channel.send(f'Added "{item}" to the list of items.')

    # Check if the message starts with "#remove"
    if message.content.startswith('#remove'):
        # Get the item from the message
        item = message.content[8:]

        # Get the list of items for the current channel
        channel = message.channel
        items = channel_lists.get(channel, [])

        # Remove the item from the list, if it exists
        if item in items:
            items.remove(item)
            channel_lists[channel] = items
            await message.channel.send(f'Removed "{item}" from the list of items.')
        else:
            await message.channel.send(f'Item "{item}" not found in the list of items.')

    # Check if the message is "#list"
    if message.content == '#list':
        # Get the list of items for the current channel
        channel = message.channel
        items = channel_lists.get(channel, [])

        # Create a message with the list of items
        item_list = '\n'.join(items)
        message = 'The list of items is:\n' + item_list

        # Send the message
        await message.channel.send(message)

client.run(BOT_TOKEN)