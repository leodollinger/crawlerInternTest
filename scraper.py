import asyncio
from pyppeteer import launch
import re
import collections
import json

async def getLenovoLinks():
    """
    Gets the lenovo links from webscraper.io.

    :returns:   The lenovo links.
    :rtype:     { Dict }
    """
    browser = await launch()
    page    = await browser.newPage()
    # print('Loading the page')
    await page.goto('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
    pageContent = await page.content() #get page content
    # print('getting page links')
    aTags = re.findall(r"<a(.*)>.*?|<(.*) /a>",pageContent) #regex getting all "<a>" html tags
    laptops = {}
    # getting lenovo links
    for link in aTags:
        if re.search('Lenovo', link[0], re.IGNORECASE):
            title = (re.search(r"title=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[7:-1] #get link title
            href  = "https://webscraper.io" + (re.search(r"href=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[6:-1] #get link url
            laptops[title] = href
    await browser.close()
    return laptops

async def getLaptopsData(laptopsLink):
    """
    Gets data from all given laptop links.

    :param      laptopsLink:  The laptop links
    :type       laptopsLink:  { Dict }

    :returns:   The laptops data.
    :rtype:     { Dict }
    """
    leptopsWithData = {}
    browser = await launch()
    for title in laptopsLink:
        link    = laptopsLink[title]
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
    return leptopsWithData

def orderLaptops(laptops):
    """
    { Sort a given laptop dictionary }

    :param      laptops:  The laptops dictionary
    :type       laptops:  { Dict }

    :returns:   { Sorted laptops dictionary }
    :rtype:     { Dict }
    """
    newDict = {}
    for key in sorted(laptops, key = lambda x: float(x)):
        newDict[str(key)] = laptops[str(key)]
    return newDict

def main():
    laptops = asyncio.get_event_loop().run_until_complete(getLenovoLinks())
    laptops = asyncio.get_event_loop().run_until_complete(getLaptopsData(laptops))
    laptops = orderLaptops(laptops)
    json_object = json.dumps(laptops, indent = 4) 
    print(json_object)


main()