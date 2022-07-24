from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape SUPERBET')

    # SUPERBET -- ODDS ARE SHOWN AS DUPLICATES
    LINK = 'https://superbet.ro/pariuri-sportive/fotbal'
    rows = "//div[@class='event-row']"
    Scrape(LINK, rows)

    print('Finished Scraping SUPERBET')
