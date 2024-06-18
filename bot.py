import discord
import asyncio
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time
import pytz

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = 1076166922841899119

client = discord.Client()
timezone = pytz.timezone('Europe/London')

def get_random_hadith():
    collections = [
        {'name': 'bukhari', 'max_hadith': 97},
        {'name': 'muslim', 'max_hadith': 56},
        {'name': 'nasai', 'max_hadith': 51},
        {'name': 'abudawud', 'max_hadith': 43},
        {'name': 'tirmidhi', 'max_hadith': 49},
        {'name': 'ibnmajah', 'max_hadith': 37},
        {'name': 'malik', 'max_hadith': 61},
        {'name': 'ahmad', 'max_hadith': 7}
    ]
    
    # Choose a random collection
    collection = random.choice(collections)
    collection_name = collection['name']
    
    # Choose a random Hadith number
    hadith_number = random.randint(1, collection['max_hadith'])
    
    # Fetch the random Hadith
    base_url = f'https://sunnah.com/{collection_name}/{hadith_number}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Adjust the selector based on the specific structure of each collection's page
    if collection_name in ['bukhari', 'muslim', 'nasai', 'abudawud', 'tirmidhi', 'ibnmajah']:
        hadith_text = soup.find('div', {'class': 'text_details'}).text.strip()
    elif collection_name == 'malik':
        hadith_text = soup.find('div', {'class': 'english'}).text.strip()
    elif collection_name == 'ahmad':
        hadith_text = soup.find('div', {'class': 'text'}).text.strip()
    else:
        raise ValueError(f'Collection "{collection_name}" is not supported.')

    return hadith_text

async def send_daily_hadith():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    while not client.is_closed():
        # Get current time in the specified timezone
        now = datetime.now(timezone)
        
        # Check if it's 10 PM in the specified timezone
        if now.time() == time(22, 0):  # 22:00 is 10 PM
            # Get a random Hadith
            hadith = get_random_hadith()
            
            # Send the Hadith to the Discord channel
            await channel.send(hadith)
            
            # Delay to prevent multiple messages being sent at 10 PM
            await asyncio.sleep(60)  # Sleep for 60 seconds to prevent duplicate messages
        
        # Delay to check the time again
        await asyncio.sleep(60)  # Check every 60 seconds

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.loop.create_task(send_daily_hadith())
client.run(TOKEN)
