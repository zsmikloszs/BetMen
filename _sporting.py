from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape SPORTINGBET')
    # SPORTINGBET
    LINK = "https://sports.sportingbet.ro/ro/sports/fotbal-4/ast%C4%83zi"
    rows = "//div[@class='grid-event-wrapper']"
    Scrape(LINK, rows)
    print('Finished Scraping SPORTINGBET')
