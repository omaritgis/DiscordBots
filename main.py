import discord
import random
import requests
import json
import base64
from os.path import join, dirname
from os import environ
import pygame
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = environ.get("TOKEN")
client = discord.Client()
pygame.mixer.init()


def send_request(message):
    url = "https://tobnam.herokuapp.com/api/text-to-speech"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({
        "text": f"{str(message)}"
    })
    res = requests.request("POST", url, headers=headers, data=payload)
    if res.status_code == 200:
        print(res.text)
        #fixed = res.text.replace('"}', '')
        fixed = res.text
        sound_data = base64.b64decode(fixed)
        sound = pygame.mixer.Sound(sound_data)
        ch = sound.play()
        while ch.get_busy():
            pygame.time.wait(100)
    else:
        print("Aint nuthing but a g-thang babyy!")


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"Hello, {username}: {user_message} ({channel})")

    if message.author == client.user:
        return

    if message.channel.name == 'general':
        if user_message.lower() == 'help':
            await message.channel.send(f"Hello {username}")
            return
        if "grep" in user_message.lower():
            # print message history for the channel
            user_message = user_message.replace("grep", "")
            chan = discord.utils.get()
            messages = await chan.history(limit=200).flatten()
            print(messages)
        if "--tts" in user_message.lower():
            user_message = user_message.replace("--tts", "")
            send_request(user_message)


client.run(TOKEN)
