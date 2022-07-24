from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape 888')
    # 888 SPORT # BUGOS - KELL MENU NYITOGATOT CSINALNI - NEM FONTOS
    LINK = 'https://www.888sport.ro/fotbal/#/filter/football'
    rows = "//li[contains(@class,'KambiBC-event-item')]"
    Scrape(LINK, rows)
    print('Finished Scraping 888')
