import asyncio
from pyppeteer import launch

import re
import json

import time

async def getLenovoLinks(url, debug = False):
    """
    Gets the lenovo links from given url.
    
    :param      url:    The page url
    :type       url:    String
    :param      debug:  Control variable to show or not progress comments
    :type       debug:  bool
    
    :returns:   The lenovo links.
    :return type:     Dict
    """
    browser = await launch()
    page    = await browser.newPage()
    if debug:
        print(f'Connecting to {url}')
    await page.goto(url)
    pageContent = await page.content() #get page content
    if debug:
        print('Getting all page <a> tags')
    aTags = re.findall(r"<a(.*)>.*?|<(.*) /a>",pageContent) #regex getting all "<a>" html tags
    laptops = {}
    # getting lenovo links
    if debug:
        print('Getting all Lenovo links and titles')
    for link in aTags:
        if re.search('Lenovo', link[0], re.IGNORECASE):
            title = (re.search(r"title=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[7:-1] #get link title
            href  = "https://webscraper.io" + (re.search(r"href=([\"'])(?:(?=(\\?))\2.)*?\1",link[0]).group())[6:-1] #get link url
            laptops[title] = href
    await browser.close()
    return laptops

async def getLaptopsData(laptopsLink, debug = False):
    """
    Gets data from all given laptop links.
    
    :param      laptopsLink:  The laptop links
    :type       laptopsLink:  Dict
    :param      debug:        Control variable to show or not progress comments
    :type       debug:        bool
    
    :returns:   The laptops data.
    :return type:     Dict
    """
    leptopsWithData = {}
    browser = await launch()
    for title in laptopsLink:
        link    = laptopsLink[title]
        page    = await browser.newPage()
        if debug:
            print(f'Getting "{title}" data.')
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

def orderLaptops(laptops, debug = False):
    """
    Sort a given laptop dictionary
    
    :param      laptops:  The laptops dictionary
    :type       laptops:  Dict
    :param      debug:    Control variable to show or not progress comments
    :type       debug:    bool
    
    :returns:   Sorted laptops dictionary
    :return type:     Dict
    """
    newDict = {}
    if debug:
        print('Starting sorting')
    for key in sorted(laptops, key = lambda x: float(x)):
        newDict[str(key)] = laptops[str(key)]
    if debug:
        print('Sorting done!')
    return newDict

def getLenovoLaptopsJson(url, debug = False):
    """
    Gets all lenovo laptops from given link, sort it by price (low priced to high priced) and gets all of its data
    
    :param      url:    The page url
    :type       url:    String
    :param      debug:  Control variable to show or not progress comments
    :type       debug:  bool
    
    :returns:   The lenovo laptops json.
    :return type:     String
    """
    if debug:
        start = time.time()
    laptops = asyncio.get_event_loop().run_until_complete(getLenovoLinks(url, debug))
    laptops = asyncio.get_event_loop().run_until_complete(getLaptopsData(laptops, debug))
    laptops = orderLaptops(laptops, debug)
    json_object = json.dumps(laptops, indent = 4)
    if debug:
        end = time.time()
        print(f'Run time is: {end-start}')
    return json_object

def main():
    json_object = getLenovoLaptopsJson('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
    print(json_object)


main()