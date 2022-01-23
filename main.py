import os
from dotenv import load_dotenv
import requests
import discord

load_dotenv()

ROTATION_API_KEY = os.getenv('ROTATION_API_KEY')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

webhook = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())

response = requests.get(f'https://api.mozambiquehe.re/crafting', params={'auth': ROTATION_API_KEY})
bundles = response.json()

def run():
    for bundle in bundles:
        bundle_type = bundle['bundleType']
        bundle_contents = bundle['bundleContent']
        if bundle_type != 'daily' and bundle_type != 'weekly':
            continue

    webhook.send(content=bundle_type)

    for bundle_content in bundle_contents:
        embed = discord.Embed()
        embed.title = f'{bundle_content["itemType"]["name"]}({bundle_content["cost"]})'
        embed.color = int(bundle_content["itemType"]["rarityHex"][1:], 16)
        embed.set_image(url=bundle_content["itemType"]["asset"])

        webhook.send(embed=embed)
