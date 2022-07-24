from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape eFORTUNA')

    ## EFORTUNA # BUGGOS # NINCS CSAPAT NEV
    LINK = "https://efortuna.ro/pariuri-online/fotbal"
    rows = "//tr[@class='tablesorter-hasChildRow']"
    Scrape(LINK, rows)

    print('Finished Scraping eFORTUNA')
