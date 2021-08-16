import asyncio
from pyppeteer import launch

import re
import json

import time

from flask import Flask
from flask_restplus import Api, Resource

from src.server.instance import server

app = server.app
api = server.api


@api.route('/laptops')
class LaptopList(Resource):
    def get(self,):
        asyncio.set_event_loop(asyncio.new_event_loop())
        json_object = asyncio.get_event_loop().run_until_complete(self.scraper())
        return json_object

    async def scraper(self,):
    # parte 1 - init
        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
        page    = await browser.newPage()

        await page.goto('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
        pageContent = await page.content() #get page content

        aTags = re.findall(r"<a(.*)>.*?|<(.*) /a>",pageContent) #regex getting all "<a>" html tags
        laptops = {}
        # getting lenovo links

        for link in aTags:
            if re.search('Lenovo', link[0], re.IGNORECASE):
                title = (re.search(r"title=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[7:-1] #get link title
                href  = "https://webscraper.io" + (re.search(r"href=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[6:-1] #get link url
                laptops[title] = href

        await browser.close()
    # parte 1 - end
    # parte 2 - init
        leptopsWithData = {}
        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
        for title in laptops:
            link    = laptops[title]
            page    = await browser.newPage()

            await page.goto(link)
            pageContent = await page.content() #get page content
            description = (re.search(r"<p class=\"description\"(.*)>.*?|<(.*) /p>",pageContent).group())[23:-4]
            price       = (re.search(r"<h4 class=\"pull-right price\"(.*)>.*?|<(.*) /h4>",pageContent).group())[30:-5]
            starsNumber = len(re.findall(r"<span class=\"glyphicon glyphicon-star\"(.*)>.*?|<(.*) /span>", pageContent))
            leptopsWithData[str(price)] = {
                title:{
                        'description': description,
                        'prices': {
                                    'HDD-128': float(price),
                                    'HDD-256': float(price)+20,
                                    'HDD-512': float(price)+40,
                                    'HDD-1024': float(price)+60
                                  },
                        'starsNumber': starsNumber,
                        'link': link}
            }
        await browser.close()
    # parte 2 - end
    # parte 3 - init
        newDict = {}
        for key in sorted(leptopsWithData, key = lambda x: float(x)):
            newDict[str(key)] = leptopsWithData[str(key)]
        return newDict
    # parte 3 - end