from magicScraper import *

if __name__ == '__main__':
    # betano
    print('Starting to Scrape Betano')
    LINK = 'https://ro.betano.com/sport/fotbal/urmatoarele-12-ore/'
    rows = "//tr[@class='events-list__grid__event']"
    rows = "//tr[contains(@data-qa,'pre-event')]"
    Scrape(LINK, rows)
    print('Finished Scraping Betano')