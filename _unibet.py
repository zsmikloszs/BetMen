from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape UniBet')
    LINK = 'https://www.unibet.ro/betting/sports/starting-soon'
    rows = "//li[@class='KambiBC-sandwich-filter__event-list-item']"
    Scrape(LINK, rows)
    print('Finished Scraping UniBet')
