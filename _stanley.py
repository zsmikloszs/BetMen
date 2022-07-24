from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape casapariurilor')

    ## STANLEYBET -- NINCS LINK
    LINK = 'https://www.stanleybet.ro/pariuri-sportive#filter/football'
    rows = "//div[@class='KambiBC-event-item__event-wrapper']"
    Scrape(LINK, rows)


    print('Finished Scraping casapariurilor')
