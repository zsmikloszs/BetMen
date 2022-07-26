from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape UniBet')
    LINK = 'https://www.unibet.ro/betting/sports/filter/football/all/matches'
    #rows = "//div[@class='KambiBC-sandwich-filter__event-list-item']"
    rows = "//div[contains(@data-test-name,'matchEvent')]"
    Scrape(LINK, rows)
    print('Finished Scraping UniBet')
