import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import pickle

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





bookies = []
def Scrape(LINK, rows):
    options = Options()
 #   options.add_argument("window-size=2560,1080")
    #options.headless = True
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    path = r'/root/tests/chromedriver'  # introduce your file's path inside '...'
    driver = webdriver.Chrome(path, options=options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def understandRow(line):
        if '-' in line:
            line = line.replace('-', '\n')
        line = line.replace(' ', '')
        odds = re.findall(r"-?\d+(?:\.\d+)", str(line))
        lines = line.split('\n')
        toExclude = ['Ambeleechipeînscriu','TotalgoluriPeste/Sub', 'Rezultatfinal', 'MAI MULTE PARIURI', 'Playmaker', 'Live', 'meciul', 'Peste', 'Sub', 'P', 'S', 'Da', 'Nu', 'LIVE', 'Pauză', 'VorIntraÎnDesfăşurare', 'HT', 'X'] + odds

        excludedList = [element for element in lines if element not in toExclude]
        def clearString(data):
            specialChars = ['IUL', 'Începeîn', 'meciul', ':', '(', ')', 'CREAȚIUNPARIU', 'min', '.', 'SÂM', 'DUM', 'LUN', 'MIE', 'JOI', 'VIN', 'Mâine', 'SUSPENDAT', '/', '+', 'BETBUILDER', ',', 'AUG', 'MAIMULTEPARIURI', 'OFERTAEXTINSALIVE', 'ASTĂZI', 'PARIAZĂACUM']
            for specialChar in specialChars:
                data = data.lower().replace(specialChar.lower(), '')
            data = ''.join([i for i in data if not i.isdigit()])
            return data
        newList = []
        for exclude in excludedList:
            newList.append(clearString(exclude))
        excludedList = [x for x in newList if x != '']
       # excludedList = [x for x in excludedList if ':' not in x]
        excludedList = [element.upper() for element in excludedList]
        teams = '\n'.join(excludedList)
        return teams, odds
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    def areOdds():
        pass
    def arePlayers():
        pass
    bookie = LINK.split('/')[2]
    totalTeams = []
    totalOdds = []
    totalLinks = []

    driver.get(LINK)
    time.sleep(35)
    time.sleep(5)
    if bookie == 'www.unibet.ro':
        driver.find_element(By.XPATH, "//button[text()='Permitere toate']").click()
    ### WAIT UNTIL ROW APPEARS !!!
    lines = driver.find_elements(By.XPATH, rows)

    #lines = WebDriverWait(box, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, rows)))
    #email = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, rows)))

    for line in lines:
      #  print(line.text)
        teams, odds = understandRow(line.text)
        betLink = [bet.get_attribute('href') for bet in line.find_elements(By.TAG_NAME, "a")]
        # print(teams,odds)
        if teams is None:
            # ADD STAT
            continue
        if bookie == 'www.betfair.ro':
            if len(odds) > 3:
                odds = odds[-3:]
        if bookie == 'superbet.ro':
            odds = list(dict.fromkeys(odds))


        if len(odds) >= 3:
      #      print(findMatch, findOdds)
            if (isfloat(odds[0]) is True) and (isfloat(odds[1]) is True) and (isfloat(odds[2]) is True):
                formattedOdds = '\n'.join([odds[0], odds[1], odds[2]])
        #        print(teams, ' ', formattedOdds)
                totalOdds.append(formattedOdds)
                totalTeams.append(teams)
                totalLinks.append(betLink)
        elif len(odds) <= 2:
            # ADD STAT
            continue
    prepareData(totalTeams, totalOdds, bookie, 'threeWay', '1x2', totalLinks)


def prepareData(teams, odds, bookie, type, game, betLinks):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # Storing lists within dictionary
    dict_gambling = {'bookieName': bookie, 'Teams': teams, game: odds, 'betLink': betLinks}
    # Presenting data in dataframe
    bookieData = pd.DataFrame.from_dict(dict_gambling)
    if bookieData.empty:
        ### GIVE TO STAT
        return
    # clean leading and trailing whitespaces of all odds
    bookieData = bookieData.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    bookieData = bookieData[['Teams', game]]
    bookieData = bookieData.replace(r'', '0\n0', regex=True)  # odds with no values
    bookieData = bookieData.replace(r'^\d+\.\d+$', '0\n0', regex=True)  # odds with only one element
    save = '_temp/' + bookie+'.pkl'
    with open(save, 'wb') as output:
        pickle.dump(bookieData, output)
        bookies.append(save)

    return bookieData

#if __name__ == "__main__":
 #   Scrape(LINK, rows, match, odds)