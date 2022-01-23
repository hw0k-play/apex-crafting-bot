import os
from dotenv import load_dotenv
import requests
import discord
import json


load_dotenv()

ROTATION_API_KEY = os.getenv('ROTATION_API_KEY')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def run(event, context):
    webhook = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())

    response = requests.get(f'https://api.mozambiquehe.re/crafting', params={'auth': ROTATION_API_KEY})
    bundles = response.json()

    for bundle in bundles:
        bundle_type = bundle['bundleType']
        bundle_contents = bundle['bundleContent']
        if bundle_type != 'daily' and bundle_type != 'weekly':
            continue

        embeds = []
        for bundle_content in bundle_contents:
            embed = discord.Embed()
            embed.title = f'{bundle_content["itemType"]["name"]}({bundle_content["cost"]})'
            embed.color = int(bundle_content["itemType"]["rarityHex"][1:], 16)
            embed.set_image(url=bundle_content["itemType"]["asset"])

            embeds.append(embed)
    
        webhook.send(content=bundle_type, embeds=embeds)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello"
        }),
    }
