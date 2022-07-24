from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape casapariurilor')

    # CASA PARIURILOR
    LINK = 'https://www.casapariurilor.ro/pariuri-online/fotbal'
    rows = "//tr[@class='tablesorter-hasChildRow']"
    Scrape(LINK, rows)

    print('Finished Scraping casapariurilor')
