import asyncio

import requests
#from NHentai import NHentaiAsync

#parser = NHentaiAsync()

async def main():
    # doujin = await parser.get_doujin(300000)
    # print(doujin)
    resp = requests.get("https://rule34.xxx")
    print(resp.status_code)

asyncio.run(main())
