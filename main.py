import subprocess
import pandas as pd
import pickle
from magicScraper import *
#from surebet import *
import swifter

import pandas as pd
from fuzzywuzzy import process, fuzz
from sympy import symbols, Eq, solve
import itertools
import datetime
import time
import functools
import swifter
import concurrent.futures

import requests


dict_surebet= {}
total_stake = 500 # RON

def telegram_bot_sendtext(bot_message):

   bot_token = '5559348678:AAE5F3A0YiY9rn6lko1Rd3NI9G2SVazS_hQ'
   bot_chatID = '5213933251'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + str(bot_message)

   response = requests.get(send_text)

   return response.json()

def surebet(frame, dictName):

    frame[['1x2_1_a', '1x2_X_a', '1x2_2_a']] = frame['1x2_x'].apply(lambda x: x.split('\n')).apply(pd.Series).astype(
        float)
    frame[['1x2_1_b', '1x2_X_b', '1x2_2_b']] = frame['1x2_y'].apply(lambda x: x.split('\n')).apply(pd.Series).astype(
        float)
    frame[['1x2_1_c', '1x2_X_c', '1x2_2_c']] = frame['1x2'].apply(lambda x: x.split('\n')).apply(pd.Series).astype(
        float)
    frame['sure_var1'] = (1 / frame['1x2_1_a']) + (1 / frame['1x2_X_b']) + (1 / frame['1x2_2_c'])

    frame = frame[
        ['Teams_x', '1x2_x', 'Teams_y', '1x2_y', 'Teams', '1x2', 'sure_var1', '1x2_1_a', '1x2_X_a', '1x2_2_a', '1x2_1_b', '1x2_X_b', '1x2_X_b', '1x2_1_c',
         '1x2_X_c', '1x2_2_c']]
    frame = frame[
        (frame['sure_var1'] < 1)]
    frame.reset_index(drop=True, inplace=True)
    print(frame)
    print(dict_surebet)
    for i, value in dict_surebet[dictName]['sure_var1'].items():
        if value < 1:
            bookies = dictName.split('\n')
            odds1 = float(dict_surebet[dictName].at[i,'1x2_1_a'])
            print(odds1)
            odds2 = float(dict_surebet[dictName].at[i,'1x2_X_b'])
            odds3 = float(dict_surebet[dictName].at[i,'1x2_2_c'])
            oddsList = '\n'.join([str(odds1), str(odds2), str(odds3)])
            teamsA = dict_surebet[dictName].at[i, 'Teams_x'].replace('\n', '  -  ')
            teamsB = dict_surebet[dictName].at[i, 'Teams_y'].replace('\n', '  -  ')
            teamsC = dict_surebet[dictName].at[i, 'Teams'].replace('\n', '  -  ')
            bookiesA = bookies[0].replace('_', '').replace('temp/', '')
            bookiesB = bookies[1].replace('_', '').replace('temp/', '')
            bookiesC = bookies[2].replace('_', '').replace('temp/', '')

            results = beat_bookies(odds1, odds2, odds3, total_stake)
            if float(results['Benefit1'].replace('%', '')) >= 10:
                telegram_bot_sendtext(
                    f"Benefit {results['Benefit1']} and {results['Profit1']} RON profit on every {total_stake} RON with:\n"
                    f"- {bookiesA} -\n    OD 1: {odds1}    PUT:{results['Stakes1']} RON\n    {teamsA}\n    EXPECTED PAYOUT: {results['Payout1']} RON\nLINK: \n\n"
                    f"- {bookiesB} -\n    OD X: {odds2}    PUT:{results['Stakes2']} RON\n    {teamsB}\n    EXPECTED PAYOUT: {results['Payout2']} RON\nLINK: \n\n"
                    f"- {bookiesC} -\n    OD 2: {odds3}    PUT:{results['Stakes3']} RON\n    {teamsC}\n    EXPECTED PAYOUT: {results['Payout3']} RON\nLINK: \n\n")

    return frame


def prettyResults(dict_surebet, frame, result, od1, odX, od2):
    total_stake = 500

    bookies = frame.split('\n')
    odds1 = float(dict_surebet[frame].at[i, od1])
    odds2 = float(dict_surebet[frame].at[i, odX])
    odds3 = float(dict_surebet[frame].at[i, od2])
    oddsList = '\n'.join([str(odds1), str(odds2), str(odds3)])
    teamsA = dict_surebet[frame].at[i, 'Teams_x'].replace('\n', '  -  ')
    teamsB = dict_surebet[frame].at[i, 'Teams_y'].replace('\n', '  -  ')
    teamsC = dict_surebet[frame].at[i, 'Teams'].replace('\n', '  -  ')
    bookiesA = bookies[0].replace('_', '').replace('temp/', '')
    bookiesB = bookies[1].replace('_', '').replace('temp/', '')
    bookiesC = bookies[2].replace('_', '').replace('temp/', '')

    results = beat_bookies(odds1, odds2, odds3, total_stake)
    if float(results['Benefit1']) >= 10:

        telegram_bot_sendtext(f"Benefit {results['Benefit1']} and {results['Profit1']} RON profit on every {total_stake} RON with:\n"
                              f"- {bookiesA} -\n    OD 1: {odds1}    PUT:{results['Stakes1']} RON\n    {teamsA}\n    EXPECTED PAYOUT: {results['Payout1']} RON\nLINK: \n\n"
                              f"- {bookiesB} -\n    OD X: {odds2}    PUT:{results['Stakes2']} RON\n    {teamsB}\n    EXPECTED PAYOUT: {results['Payout2']} RON\nLINK: \n\n"
                              f"- {bookiesC} -\n    OD 2: {odds3}    PUT:{results['Stakes3']} RON\n    {teamsC}\n    EXPECTED PAYOUT: {results['Payout3']} RON\nLINK: \n\n")

#            firstSeen = datetime.datetime.now()
#            lastSeen = firstSeen
#
#                difference = lastSeen - firstSeen
##               seconds = difference.total_seconds()
#             odds = ' '.join(str(od) for od in [odds1,odds2,odds3])
#            dict = {'Teams': [teams], 'Benefit': '39%','LAY_MIDDLE_BACK': [odds], 'First Seen': firstSeen.isoformat(),'LastSeen': lastSeen.isoformat(), 'Elapsed Time': seconds}
#           dict = pd.DataFrame(dict)
#          dict.to_csv('_stats.csv', mode='a', index=False, header=False)


# def continueWorkingWithStats():
#     try:
#         stats = pd.read_csv('_stats.csv', names=['Teams', 'Benefit', 'LAY_MIDDLE_BACK', 'First Seen', 'LastSeen','Elapsed Time'])
#     except:
#        # stats = pd.DataFrame(index=['Teams', 'Benefit', 'LAY_MIDDLE_BACK', 'First Seen', 'LastSeen','Elapsed Time'])
# stats.to_csv('_stats.csv', mode='wb', index=False, header=True)
#         dict.to_csv('_stats.csv', mode='a', index=False, header=False)
#   stats = pd.read_csv('_stats.csv', names=['Teams', 'Benefit', 'LAY_MIDDLE_BACK', 'First Seen', 'LastSeen','Elapsed Time'])

#    if ( teamS in list(stats['Teams'])):###and
# odds in list(stats['LAY_MIDDLE_BACK']) == odds
#       firstSeen = datetime.datetime.now()
#      lastSeen = firstSeen
#     difference = lastSeen - firstSeen
#    seconds = difference.total_seconds()


#          with open('statsFrame', 'rb*') as output:
#              bookieData = pickle.load(sureData)
#        ## ADD RESULT TO statsFrame
#     elif result in statistics:
#       lastSeen = datetime.datetime.now()
#      difference = lastSeen - firstSeen
#     seconds = difference.total_seconds()
#    mins = seconds/60
# find current row and modify last seen to curren time

def beat_bookies(odds1, odds2, odds3, total_stake):
    totalProbability = 1 / odds1 + 1 / odds2 + 1 / odds3
    stakesX = (total_stake * (1 / odds1)) / totalProbability
    stakesY = (total_stake * (1 / odds2)) / totalProbability
    stakesZ = (total_stake * (1 / odds3)) / totalProbability
    profit1 = float(odds1) * float(stakesX) - float(total_stake)
    profit2 = odds2 * stakesY - total_stake
    profit3 = odds3 * stakesZ - total_stake
    total_investment = stakesX + stakesY + stakesZ
    benefit1 = f'{profit1 / total_investment * 100:.2f}%'
    benefit2 = f'{profit2 / total_investment * 100:.2f}%'
    benefit3 = f'{profit3 / total_investment * 100:.2f}%'
    payout1 = stakesX * odds1
    payout2 = stakesY * odds2
    payout3 = stakesZ * odds3
    dict_gabmling = {'Odds1': odds1, 'Odds2': odds2, 'Odds3': odds3, 'Stakes1': f'{stakesX:.0f}',
                     'Stakes2': f'{stakesY:.0f}', 'Stakes3': f'{stakesZ:.0f}', 'Profit1': f'{profit1:.2f}',
                     'Profit2': f'{profit2:.2f}', 'Profit3': f'{profit3:.2f}',
                     'Benefit1': benefit1, 'Benefit2': benefit2, 'Benefit3': benefit3, 'Payout1': f'{payout1:.2f}',
                     'Payout2': f'{payout2:.2f}', 'Payout3': f'{payout3:.2f}'}
    return dict_gabmling


# for bookie in y:
def matchTeams(bookie, preparedData):
    bookieA = bookie[0]
    bookieB = bookie[1]
    bookieC = bookie[2]

    df1 = preparedData[bookieA].copy()
    df2 = preparedData[bookieB].copy()
    df3 = preparedData[bookieC].copy()
    teams_2 = df2['Teams'].tolist()
    teams_3 = df3['Teams'].tolist()

    df1[['Teams_matched_' + bookieB, 'Score_' + bookieB]] = df1['Teams'].swifter.apply(
        lambda x: process.extractOne(x, teams_2, scorer=fuzz.token_set_ratio)).apply(pd.Series)
    df1[['Teams_matched_' + bookieC, 'Score_' + bookieC]] = df1['Teams'].swifter.apply(
        lambda x: process.extractOne(x, teams_3, scorer=fuzz.token_set_ratio)).apply(pd.Series)
    df_surebet = df1.merge(df2, left_on='Teams_matched_' + bookieB, right_on='Teams').merge(df3,
                                                                                            left_on='Teams_matched_' +
                                                                                                    bookie[2],
                                                                                            right_on='Teams')
    df_surebet = df_surebet[df_surebet['Score_' + bookieB] > 90]
    df_surebet = df_surebet[df_surebet['Score_' + bookieC] > 90]
    df_surebet = df_surebet[['Teams_x', '1x2_x', 'Teams_y', '1x2_y', 'Teams', '1x2']]
    dictName = bookieA + "\n" + bookieB + "\n" + bookieC
    if not df_surebet.empty:
        dict_surebet[dictName] = df_surebet
        return surebet(df_surebet, dictName)


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#scrape in parallel (at the same time)
#subprocess.run("python3 bookie1_tipico_live.py & python3 bookie2_bwin_live.py & python3 bookie3_betfair_live.py & wait", shell=True)



def main():
    # UNIBET
    LINK = 'https://www.unibet.ro/betting/sports/starting-soon'
    rows = "//li[@class='KambiBC-sandwich-filter__event-list-item']"
    Scrape(LINK, rows)

    # betano
    LINK = 'https://ro.betano.com/sport/fotbal/urmatoarele-12-ore/'
    rows = "//tr[@class='events-list__grid__event']"
    rows = "//tr[contains(@data-qa,'pre-event')]"
    Scrape(LINK, rows)

    ## betfair
    LINK = 'https://www.betfair.ro/sport/football'
    rows = "//li[contains(@class,'com-coupon-line')]"
    Scrape(LINK, rows)

    # 888 SPORT # BUGOS - KELL MENU NYITOGATOT CSINALNI - NEM FONTOS
    LINK = 'https://www.888sport.ro/fotbal/#/filter/football'
    rows = "//li[contains(@class,'KambiBC-event-item')]"
    Scrape(LINK, rows)

    ## EFORTUNA # BUGGOS # NINCS CSAPAT NEV
    LINK = "https://efortuna.ro/pariuri-online/fotbal"
    rows = "//tr[@class='tablesorter-hasChildRow']"
    Scrape(LINK, rows)

    ### ADMIRAL
    LINK = 'https://www.admiral.ro/ro/sporturi#sports-hub/football/romania/liga_i'
    rows = "//li[@class='KambiBC-sandwich-filter__event-list-item']"
    Scrape(LINK, rows)

    # CASA PARIURILOR
    LINK = 'https://www.casapariurilor.ro/pariuri-online/fotbal'
    rows = "//tr[@class='tablesorter-hasChildRow']"
    Scrape(LINK, rows)

    ## STANLEYBET -- NINCS LINK
    LINK = 'https://www.stanleybet.ro/pariuri-sportive#filter/football'
    rows = "//div[@class='KambiBC-event-item__event-wrapper']"
    Scrape(LINK, rows)

    # SUPERBET -- ODDS ARE SHOWN AS DUPLICATES
    LINK = 'https://superbet.ro/pariuri-sportive/fotbal'
    rows = "//div[@class='event-row']"
    Scrape(LINK, rows)

    # SPORTINGBET
    LINK = "https://sports.sportingbet.ro/ro/sports/fotbal-4/ast%C4%83zi"
    rows = "//div[@class='grid-event-wrapper']"
    Scrape(LINK, rows)

    # NETBET -- AD ODDSOKAT AT KELL ALAKITANI EU-RA
    LINK = 'https://sport.netbet.ro/en-ro/'
    rows = "//div[@class='rj-ev-list__ev-card__inner']"
    #Scrape(LINK, rows)

  #  threeWay(preparedData)

def trial():

    ## WINMASTERS # JS FAIL ########
    LINK = 'https://www.winmasters.ro/ro/sports/i/'
    rows = "//div[@class='MatchListGroup__Content']//div"

    ## MAXBET.RO # SAME AS WINMASTERS !
    LINK = 'https://www.maxbet.ro/ro/pariuri'
    rows = "//div[@class='EventItem']"
    odds =  ''### '3.90\n2.25\n2.45'
    betLink = '' ### 'https://live.efortuna.ro/meci/LROFOOTBALL/LRO3368148'



    Scrape(LINK, rows, match, odds)
    TEAMS = ['Faska1Romaniaaaaa', 'nemteny', 'teny']
    ODDS = ['11.1\n11.2\n11.3\n', '1.1\n1.2\n1.3\n', '1.1\n3.1\n1.1\n' ]
    bookie = 'futura.ro'
    prepareData(TEAMS, ODDS, bookie, '', '1x2')

    TEAMS = ['Faska2Hunggggeery', 'nemteny', 'teny']
    ODDS = ['11.1\n11.2\n11.3\n', '1.1\n1.2\n1.3\n', '5.2\n1.2\n1.2\n' ]
    bookie = 'kutura.ro'
    prepareData(TEAMS, ODDS, bookie, '', '1x2')

    TEAMS = ['Faska3', 'nemteny', 'teny']
    ODDS = ['11.1\n11.2\n11.3\n', '1.1\n1.2\n1.3\n', '1.3\n1.3\n4.3\n' ]
    bookie = 'mutura.ro'
    preparedData = {}

    prepareData(TEAMS, ODDS, bookie, '', '1x2')
    threeWayData = ['mutura.ro.pkl', 'kutura.ro.pkl', 'futura.ro.pkl']
    for three in threeWayData:
        data=  pickle.load(open(three, 'rb'))
        preparedData[three] = data
    threeWay(preparedData)



if __name__ == '__main__':
    t1 = time.perf_counter()
    #main() #$$ RETURN BOOKIES
    preparedData = {}
    bookies = ['_temp/efortuna.ro.pkl', '_temp/ro.betano.com.pkl', '_temp/sports.sportingbet.ro.pkl', '_temp/superbet.ro.pkl', '_temp/www.888sport.ro.pkl', '_temp/www.admiral.ro.pkl', '_temp/www.betfair.ro.pkl', '_temp/www.casapariurilor.ro.pkl', '_temp/www.stanleybet.ro.pkl', '_temp/www.unibet.ro.pkl' ]
    for booki in bookies:
        data = pickle.load(open(booki, 'rb'))
        preparedData[booki] = data

    listList = list(itertools.product(preparedData, preparedData, preparedData))
    y = [s for s in listList if s[0] != s[1] and s[1] != s[2] and s[0] != s[2]]

    for boo in y:
        matchTeams(boo, preparedData)
  #  with concurrent.futures.ProcessPoolExecutor() as executor:
  ##      for boo in y:
  #          executor.submit(matchTeams, boo, preparedData)
    #     partial_sum_four = functools.partial(matchTeams, y, preparedData)
    #     executor.submit(matchTeams, partial_sum_four)


    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
