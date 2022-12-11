import os
import discord
import json

BOT_TOKEN = os.environ.get('LISTY_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# The file to save and load the lists of items from
LISTS_FILE = '/bots/listy/data/lists.json'

# A dictionary to store the lists of items for each channel
channel_lists = {}

def save_lists():
    # Save the channel lists to the JSON file
    with open(LISTS_FILE, 'w') as f:
        json.dump(channel_lists, f)

def load_lists():
    # Load the channel lists from the JSON file, if it exists
    try:
        with open(LISTS_FILE, 'r') as f:
            lists = json.load(f)
    except FileNotFoundError:
        # Create a new JSON file if it does not exist
        with open(LISTS_FILE, 'w') as f:
            lists = {}

    return lists

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Load the lists of items from the JSON file
    global channel_lists
    channel_lists = load_lists()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message starts with "#add"
    if message.content.startswith('#add'):
        # Get the item and genres from the message
        parts = message.content[5:].split(' ', 1)
        item = parts[0]
        genres = []
        if len(parts) > 1:
            genres = parts[1].split()

        # Get the list of items for the current channel
        channel = str(message.channel)
        items = channel_lists.get(channel, [])

        # Add the item to the list
        items.append({'name': item, 'genres': genres})

        # Store the list of items for the current channel
        channel_lists[channel] = items

        # Save the updated lists to the JSON file
        save_lists()

        if len(genres) == 0:
            await message.channel.send(f'Added "{item}" to the list of items.')
        else:
            await message.channel.send(f'Added "{item}" with genres "{", ".join(genres)}" to the list of items.')

    # Check if the message starts with "#remove"
    if message.content.startswith('#remove'):
        # Get the item from the message
        item = message.content[8:]

        # Get the list of items for the current channel
        channel = str(message.channel)
        items = channel_lists.get(channel, [])

        # Remove the item from the list, if it exists
        for i, item_dict in enumerate(items):
            if item_dict['name'] == item:
                del items[i]
                channel_lists[channel] = items

                # Save the updated lists to the JSON file
                save_lists()

                await message.channel.send(f'Removed "{item}" from the list of items.')
                return
        else:
            await message.channel.send(f'Item "{item}" not found in the list of items.')

    # Check if the message starts with "#edit"
    if message.content.startswith('#edit'):
        # Get the item and new genres from the message
        parts = message.content[6:].split(' ', 1)
        item = parts[0]
        genres = []
        if len(parts) > 1:
            genres = parts[1].split()

        # Get the list of items for the current channel
        channel = str(message.channel)
        items = channel_lists.get(channel, [])

        # Edit the item in the list, if it exists
        for i, item_dict in enumerate(items):
            if item_dict['name'] == item:
                item_dict['genres'] = genres
                channel_lists[channel] = items

                # Save the updated lists to the JSON file
                save_lists()

                if len(genres) == 0:
                    await message.channel.send(f'Removed the genres of "{item}".')
                else:
                    await message.channel.send(f'Set the genres of "{item}" to "{", ".join(genres)}".')
                return
        else:
            await message.channel.send(f'Item "{item}" not found in the list of items.')

    # Check if the message starts with "#list"
    if message.content.startswith('#list'):
        # Get the list of items for the current channel
        channel = str(message.channel)
        items = channel_lists.get(channel, [])

        # Get the genres to filter the list by, if specified
        genres = message.content[6:].split()

        # Build the list of items to display
        display_items = []
        for item in items:
            if set(genres).issubset(item['genres']):
                display_items.append(item['name'])

        if len(display_items) == 0:
            await message.channel.send('No items found in the list.')
        else:
            await message.channel.send('\n'.join(display_items))

client.run(BOT_TOKEN)