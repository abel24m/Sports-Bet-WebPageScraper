from pick_handler import Pick_Handler, League
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import date
from database import enter_picks_into_database
import re

phand = Pick_Handler()

SIMILARITY_STANDARD = .80


pickswise_urls =            [
                            "https://www.pickswise.com/nba/picks/",
                            "https://www.pickswise.com/nfl/picks/",
                            "https://www.pickswise.com/nhl/picks/",
                            "https://www.pickswise.com/college-basketball/picks/",
                            "https://www.pickswise.com/college-football/picks/"
                            ]


winners_and_winers_urls =   [
                            "https://winnersandwhiners.com/games/nba/",
                            "https://winnersandwhiners.com/games/nfl/",
                            "https://winnersandwhiners.com/games/nhl/",
                            "https://winnersandwhiners.com/games/ncaab/",
                            "https://winnersandwhiners.com/games/ncaaf/"
                            ]

sportschatplace_urls =      [
                            "https://sportschatplace.com/nba-picks/page/",
                            "https://sportschatplace.com/nfl-picks/page/",
                            "https://sportschatplace.com/nhl-picks/page/",
                            "https://sportschatplace.com/college-basketball-picks/page/",
                            "https://sportschatplace.com/college-football-picks/page/"   
                            ]

docsports_urls =            [
                            "https://www.docsports.com/free-picks/nba/",
                            "https://www.docsports.com/free-picks/nfl/",
                            "https://www.docsports.com/free-picks/nhl-hockey/",
                            "https://www.docsports.com/free-picks/ncaa-college-basketball/",
                            "https://www.docsports.com/free-picks/football/"
                            ]

statsalt_urls =             [
                            "https://statsalt.com/games/nba/",
                            "https://statsalt.com/games/nfl/",
                            "https://statsalt.com/games/nhl/",
                            "https://statsalt.com/games/ncaab/",
                            "https://statsalt.com/games/ncaaf/"
                            ]



# This helper function takes in a url and perfroms the http request 
# and uses BeautifulSoup to parse the html into objects. 
# If the request fails we will return false. 
def grab_the_soup(url) :
        #build request with url provided. Use User-Agent to bypass website security. 
        req = Request(url = url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            page = urlopen(req)
        except :
            print("Issue when requesting %s", url)
            return False
        #Decode the resulting webpage with default utf-8
        html_raw = page.read().decode("utf-8")
        #Beatifulsoup can convert parse raw html into objects 
        b_soup = BeautifulSoup(html_raw, "html.parser")
        return b_soup




def scrape_pickswise():
    # Iterate through every sport url 
    for index in range(len(pickswise_urls)):
        # use Beautiful to grap all html elements from url
        the_soup = grab_the_soup(pickswise_urls[index])

        #if the soup was not returned correctly we jump to the next url 
        if the_soup == False:
            continue

        # In picks wise there could be multiple picks per 'Event'. Example an Spread pick and a Total pick 
        # So we are going to grab every event so we can indetify the date for every pick. 
        allEventCards = the_soup.find_all("div", class_= "EventCardFull_eventCardFull__rY8sx global_card__QyMGe")

        # Iterate through every Event Card
        for i in range(len(allEventCards)):

            # Find the event "Date". We are looking for the keyword Toay. If its today we will proceed. If not we go to next one. 
            date = allEventCards[i].find_all("span", string="Today")

            #If date is empty then the event is not today. 
            if not date:
                continue 
            
            # Grab all the picks for the event. Sometimes pickswise has multiple picks for event. 
            # We grab all the matchups as well. Picks and Matchups are one to one. 
            allPicks = allEventCards[i].find_all("div", class_="SelectionInfo_outcome__1i6jL")
            allMatchups = allEventCards[i].find_all("span", class_="SelectionInfo_event__petE6")


            for j in range(len(allPicks)):
                # grab the string from the matchup tag
                matchup_string = allMatchups[j].text
                #grab the pick from the pick tag
                pick = allPicks[j].next.strip()
                #Pickswise could use vs or @ to write the matchup so we check for both and then we know how to split the string
                if matchup_string.find("@") < 0 :
                    matchup_list = matchup_string.split("vs")
                else:
                    matchup_list = matchup_string.split("@")
                #The away team will be the first in the list and the home will be the second. 
                away_team = matchup_list[0].strip()
                home_team = matchup_list[1].strip()
                
                #Store the list in the pick handler as away, home, pick. 
                game_data = [away_team, home_team, pick]
                #We keep a standard on the indexes of the urls so this works. 
                match index:
                    case League.NBA.value:
                        phand.nba_picks.append(game_data)
                    case League.NFL.value:
                        phand.nfl_picks.append(game_data)
                    case League.NHL.value:
                        phand.nhl_picks.append(game_data)
                    case League.NCAAB.value:
                        phand.ncaab_picks.append(game_data)
                    case League.NCAAF.value:
                        phand.ncaaf_picks.append(game_data)




        
        


def scrape_winners_and_whiners():
    # save main url that will be needed after we obtain the path for the webpage that 
    # contains the pick. So we will add the path to this string to build the url. 
    main_url = "https://winnersandwhiners.com"
    # Iterate through the urls for every sport
    for index in range(len(winners_and_winers_urls)):
        if index == 1:
            continue
        # Use Beautifulsoup to return all the raw html. 
        b_soup = grab_the_soup(winners_and_winers_urls[index])

        if b_soup == False:
            continue

        # Find the elements that contain the picks in this case it will lead to a link to the web page that contains the pick
        # both 'findall' return all the picks 
        allPicks = b_soup.find_all("div", class_="game-index-article d-flex")

        # iterate through every pick 
        for pick in allPicks:
            # Find the button that will take us to the pick
            tag = pick.find("div", string = "Prediction")
            # the parent element contains the path to the webpage
            parent = tag.parent
            # href returns the path
            path = parent['href']
            # build the full url using the main url and the path obtained
            full_url = main_url + path
            # Grab the raw html where the actual pick resides
            b_soup = grab_the_soup(full_url)

            if b_soup == False:
                continue
            # find the tag where the pick exist 
            pick_tag = b_soup.find_all("div", class_="pick d-flex align-items-center pb-3")
            matchup_tag = b_soup.find_all("span", class_="team-name team-name-nick")

            # Convert it to string and get rid of the new line character 
            pick_string= pick_tag[0].text.strip()
            away_team = matchup_tag[0].text.strip()
            home_team = matchup_tag[1].text.strip()
            pickList = list(pick_string.split(" "))
            clean_pick = ""
            for item in range(2,len(pickList)):
                clean_pick += pickList[item] + " "
            game_data = [away_team, home_team, clean_pick]
            match index:
                case League.NBA.value:
                    phand.nba_picks.append(game_data)
                case League.NFL.value:
                    phand.nfl_picks.append(game_data)
                case League.NHL.value:
                    phand.nhl_picks.append(game_data)
                case League.NCAAB.value:
                    phand.ncaab_picks.append(game_data)
                case League.NCAAF.value:
                    phand.ncaaf_picks.append(game_data)
        

def scrape_sportchatplace():
    # save main url that will be needed after we obtain the path for the webpage that 
    # contains the pick. So we will add the path to this string to build the url. 
    main_url = "https://sportschatplace.com"
    # Iterate through the urls for every sport
    for index in range(len(sportschatplace_urls)):
        # We are using this varaible to jump out of the while loop. Becuase we check to see when we have reached the point where we are looking 
        # at picks from yesterday. 
        finished = False
        # We have to load new pages to make sure we got every pick. So we are increasing the page for the url every iteration
        page_number = 1
        while(not finished):
             # Use Beautifulsoup to return all the raw html. 
            b_soup = grab_the_soup(sportschatplace_urls[index] + str(page_number))

            if b_soup == False :
                continue
            # Find the elements that contain the picks in this case it will lead to a link to the web page that contains the pick
            allPicks = b_soup.find_all("h3", class_="post-title", itemprop="name headline")
            # grab todays date and format it to match the article so we can cross check that its for todays game.
            today = date.today()
            accurate_Date = today.strftime("%m-%d-%y")
             # iterate through every pick
            for pick in allPicks:
                # split the title of the article in order to find the date
                pickSplit = list(pick.text.split(" "))
                # For the NBA NHL AND NFL the date is located in a different location of the sentence
                if (index < 3):
                    pickDate = pickSplit[len(pickSplit)-3]
                else:
                    pickDate = pickSplit[len(pickSplit)-1]
                # this was used to check we are comparing an article that has a date 
                if (pickDate[len(pickDate)-2:] == "23"):
                    # Is the article for a pick today 
                    if (accurate_Date == pickDate):
                        pick_path = pick.a['href']
                        pick_url = main_url + pick_path
                        b_soup = grab_the_soup(pick_url)

                        if b_soup == False:
                            continue

                        pick_tags = b_soup.find_all("a", class_="team-btn")
                        matchup_tag = b_soup.find("h1", class_="article-top-title block mb-1 mb-md-2", itemprop="headline")
                        # Format of match up 'Washington Wizards vs New York Knicks Prediction 11-17-23 NBA Picks'
                        # Find where the word 'Prediction' starts then i can split the begging of the sentence with the 'vs' 
                        end_index = matchup_tag.text.find("Prediction")
                        if end_index < 0 :
                            end_index = matchup_tag.text.find("prediction")
                        matchup_string = matchup_tag.text[0:end_index]
                        matchup_list = matchup_string.split("vs")
                        away_team = matchup_list[1].strip()
                        home_team = matchup_list[0].strip()
                        final_pick = pick_tags[0].text.strip()
                        game_data = [away_team, home_team, final_pick]
                        match index:
                            case League.NBA.value:
                                phand.nba_picks.append(game_data)
                            case League.NFL.value:
                                phand.nfl_picks.append(game_data)
                            case League.NHL.value:
                                phand.nhl_picks.append(game_data)
                            case League.NCAAB.value:
                                phand.ncaab_picks.append(game_data)
                            case League.NCAAF.value:
                                phand.ncaaf_picks.append(game_data)
                    elif (page_number >= 3):
                        finished = True    
            page_number += 1


def scrape_docsports():
    # save main url that will be needed after we obtain the path for the webpage that 
    # contains the pick. So we will add the path to this string to build the url. 
    main_url = "https://www.docsports.com/"
    # Iterate through the urls for every sport
    for index in range(len(docsports_urls)):
        # We are using this varaible to jump out of the while loop. Becuase we check to see when we have reached the point where we are looking 
        # at picks from yesterday. 
        # We have to load new pages to make sure we got every pick. So we are increasing the page for the url every iteration

        # Use Beautifulsoup to return all the raw html. 
        b_soup = grab_the_soup(docsports_urls[index])

        if b_soup == False:
            continue
        # Find the elements that contain the picks in this case it will lead to a link to the web page that contains the pick
        pages_scraped = 0
        while (pages_scraped < 2):
            pages_scraped += 1
            allPicks = b_soup.find_all("a", href = True, title = True, itemprop="url")

            next_url = "https:" + b_soup.find_all("a", href = True, string=re.compile('Next'))[0]['href']

            todays_date = date.today()
            todays_date = todays_date.strftime("%m/%d/%Y")

            if (index == League.NFL.value):
                pages_scraped = 2
                for pick in allPicks:
                    # Get Pick URL 
                    MONDAY = 0
                    SUNDAY = 6
                    THURSDAY = 3
                    todays_day_of_the_week = date.today().weekday()
                    pick_title = pick.text
                    
                    scrape_article = False
                    split_title_by_colon = False

                    if (todays_day_of_the_week is MONDAY):
                        if ("Monday Night" in pick_title):
                            split_title_by_colon = True
                            scrape_article = True
                    elif (todays_day_of_the_week is SUNDAY):
                        if (todays_date in pick_title or "Sunday Night" in pick_title):
                            if ("Sunday Night" in pick_title):
                                split_title_by_colon = True
                            scrape_article = True
                    elif (todays_day_of_the_week is THURSDAY):
                        if ("Thursday Night" in pick_title):
                            split_title_by_colon = True
                            scrape_article = True

                            

                    if (scrape_article):

                        if (split_title_by_colon):
                            pick_title_list = pick_title.split(":")
                            if ("at" in pick_title):
                                split_matchup = pick_title_list[1].split("at")
                            else:
                                split_matchup = pick_title_list[1].split("vs")
                        else:
                            pick_title_list = pick_title.split(",")
                            if ("at" in pick_title):
                                split_matchup = pick_title_list[0].split("at")
                            else:
                                split_matchup = pick_title_list[0].split("vs")

                        away_team = split_matchup[0].strip()
                        home_team = split_matchup[1].strip()

                        pick_url = pick['href']
                        b_soup = grab_the_soup(pick_url)

                        if b_soup == False: 
                            continue

                        author_and_date = b_soup.find("i", string=True).text

                        author_last_index = author_and_date.find("-")
                        author_first_index = author_and_date.find("by") + 2
                        author = author_and_date[author_first_index:author_last_index].strip()


                        pick_tags = b_soup.find_all("strong", string=re.compile('Pick:|Prediction:'))
                        
                        try:
                            pick_list = pick_tags[0].text.split(":")
                        except:
                            continue

                        pick = pick_list[1].strip()

                        game_data = [away_team, home_team, pick]
                        match index:
                            case League.NBA.value:
                                phand.nba_picks.append(game_data)
                            case League.NFL.value:
                                phand.nfl_picks.append(game_data)
                            case League.NHL.value:
                                phand.nhl_picks.append(game_data)
                            case League.NCAAB.value:
                                phand.ncaab_picks.append(game_data)
                            case League.NCAAF.value:
                                phand.ncaaf_picks.append(game_data)
            else:
                for pick in allPicks:
                    pick_title = pick.text
                    
                    scrape_article = False

                    if (todays_date in pick_title):
                            scrape_article = True

                    if (scrape_article):

                        
                        pick_title_list = pick_title.split(",")

                        end_index_of_matchup = pick_title_list[0].find("Prediction")
                        matchup = pick_title_list[0][0:end_index_of_matchup].strip()

                        if (" at " in pick_title):
                            split_matchup = matchup.split("at")
                        else:
                            split_matchup = matchup.split("vs")

                        away_team_split = split_matchup[0].split(" ")
                        home_team_split = split_matchup[1].split(" ")
                        away_team = ""
                        home_team = ""

                        for word in range(len(away_team_split)-1):
                            away_team += away_team_split[word] + " "

                        for word in range(len(home_team_split)-1):
                            home_team += home_team_split[word] + " "


                        away_team = away_team.strip()
                        home_team = home_team.strip()

                        pick_url = pick['href']

                        b_soup = grab_the_soup(pick_url)

                        if b_soup == False:
                            continue

                        pick_tags = b_soup.find_all("strong", string=re.compile('Pick:|Prediction:'))
                        
                        pick_list = pick_tags[0].text.split(":")

                        pick = pick_list[1].strip()

                        game_data = [away_team, home_team, pick]
                        match index:
                            case League.NBA.value:
                                phand.nba_picks.append(game_data)
                            case League.NFL.value:
                                phand.nfl_picks.append(game_data)
                            case League.NHL.value:
                                phand.nhl_picks.append(game_data)
                            case League.NCAAB.value:
                                phand.ncaab_picks.append(game_data)
                            case League.NCAAF.value:
                                phand.ncaaf_picks.append(game_data)

            b_soup = grab_the_soup(next_url)    


def scrape_statsalt():
    # save main url that will be needed after we obtain the path for the webpage that 
    # contains the pick. So we will add the path to this string to build the url. 
    main_url = "https://statsalt.com"
    # Iterate through the urls for every sport
    for index in range(len(statsalt_urls)):
        # Use Beautifulsoup to return all the raw html. 
        b_soup = grab_the_soup(statsalt_urls[index])

        if b_soup == False:
            continue

        # Find the elements that contain the picks in this case it will lead to a link to the web page that contains the pick
        # both 'findall' return all the picks 
        allPicks = b_soup.find_all("div", class_="game-index-article d-flex")

        # iterate through every pick 
        for pick in allPicks:
            # Find the button that will take us to the pick
            tag = pick.find("div", string = "Prediction")
            # the parent element contains the path to the webpage
            parent = tag.parent
            # href returns the path
            path = parent['href']
            # build the full url using the main url and the path obtained
            full_url = main_url + path
            # Grab the raw html where the actual pick resides
            b_soup = grab_the_soup(full_url)

            if (b_soup is False):
                continue
            # find the tag where the pick exist 
            pick_tag = b_soup.find_all("div", class_="pick")
            matchup_tag = b_soup.find_all("span", class_="team-name team-name-nick")

            # Convert it to string and get rid of the new line character 
            pick_string= pick_tag[0].text.strip()
            away_team = matchup_tag[0].text.strip()
            home_team = matchup_tag[1].text.strip()
            pickList = list(pick_string.split(" "))
            clean_pick = ""
            for item in range(2,len(pickList)):
                clean_pick += pickList[item] + " "
            game_data = [away_team, home_team, clean_pick]
            match index:
                case League.NBA.value:
                    phand.nba_picks.append(game_data)
                case League.NFL.value:
                    phand.nfl_picks.append(game_data)
                case League.NHL.value:
                    phand.nhl_picks.append(game_data)
                case League.NCAAB.value:
                    phand.ncaab_picks.append(game_data)
                case League.NCAAF.value:
                    phand.ncaaf_picks.append(game_data)

            


    


def main():
    scrape_pickswise()
    scrape_winners_and_whiners()
    scrape_sportchatplace()
    scrape_docsports()
    scrape_statsalt()


    phand.group_picks_nba()
    phand.group_picks_nfl()
    phand.group_picks_nhl()
    phand.group_picks_ncaaf()
    phand.group_picks_ncaab()

    enter_picks_into_database(phand)



if __name__ == "__main__":
    main()