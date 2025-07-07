import aiohttp

async def fetch_attributes(collection_slug: str):
    url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection_slug}/attributes"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data
