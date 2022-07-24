from magicScraper import *

if __name__ == '__main__':
    ## betfair
    print('Starting to Scrape Betfair')
    LINK = 'https://www.betfair.ro/sport/football'
    rows = "//li[contains(@class,'com-coupon-line')]"
    Scrape(LINK, rows)
    print('Finished Scraping Betfair')