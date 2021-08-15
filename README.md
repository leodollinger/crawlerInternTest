Crawler developed as a test for an Internship vacancy at Devnology
==================================================================

## Description

This project, gets all lenovo laptops from the webscraper.io website, sort it by price (low priced to high priced), get all of its data and return as a json.

---

## Libraries

Currently, we are using five Libraries, are they:

* Asyncio:
	Asyncio is a library to write concurrent code using the async/await syntax.
* Json:
	Json is a lightweight data interchange format inspired by JavaScript object literal syntax.
* Pyppeteer:
	Unofficial Python port of puppeteer JavaScript (headless) chrome/chromium browser automation library.
* Re:
	Provides regular expression matching operations similar to those found in Perl.
* Time:
	Provides various time-related functions.

---

## Functions

The project functionality relies on four functions (including the main). Are they:

* getLenovoLinks(url, debug = False):
    Gets the lenovo links from given url.
    
    :param url:    The page url
    :type  url:    String
    :param debug:  Control variable to show or not progress comments
    :type  debug:  bool
    
    :returns:   The lenovo links.
    :return type:     Dict

* getLaptopsData(laptopsLink, debug = False):
		Gets data from all given laptop links.
    
    :param      laptopsLink:  The laptop links
    :type       laptopsLink:  Dict
    :param      debug:        Control variable to show or not progress comments
    :type       debug:        bool
    
    :returns:   The laptops data.
    :return type:     Dict

* orderLaptops(laptops, debug = False):
		Sort a given laptop dictionary
    
    :param      laptops:  The laptops dictionary
    :type       laptops:  Dict
    :param      debug:    Control variable to show or not progress comments
    :type       debug:    bool
    
    :returns:   Sorted laptops dictionary
    :return type:     Dict

* getLenovoLaptopsJson(url, debug = False):
		Gets all lenovo laptops from given link, sort it by price (low priced to high priced) and gets all of its data
    
    :param      url:    The page url
    :type       url:    String
    :param      debug:  Control variable to show or not progress comments
    :type       debug:  bool
    
    :returns:   The lenovo laptops json.
    :return type:     String

* main():
	Calls the getLenovoLaptopsJson function and prints its return