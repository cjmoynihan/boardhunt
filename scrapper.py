"""
This file scrapes the bgg website for user ratings
"""
# imports
from requests_html import HTMLSession
import sqlite_db

# constants
test_bg = "https://boardgamegeek.com/boardgame/36218/dominion"
test_bg_ratings  = test_bg + '/ratings'
test_user = "https://boardgamegeek.com/user/Sacrilon"
test_user_owned = "https://boardgamegeek.com/collection/user/Sacrilon?own=1&subtype=boardgame&ff=1"
db = sqlite_db.DB()


def get_soup(url):
    # Gets the parse (soup) for a given website
    session = HTMLSession()
    req = session.get(url)
    req.html.render()
    return req.html


def parse_ratings(game_url):
    # Get the ratings for a given game
    # Store game name for later
    game = game_url.split('/')[-2]
    soup = get_soup(game_url)
    # Get (user, rating) pairings
    all_rating_scores = list()
    # Go to ratings
    for rating in soup.find(".summary-rating-item"):
        # Check all ratings 1-10. They are listed as classes (for example .has-rating-5 for rating 5)
        for i in range(1, 11):
            rating_score = rating.find(f".has-rating-{i}")
            if rating_score:
                rating_score = rating_score[0].text
                break
        else:
            rating_score = None
        # Get user in same div
        user = rating.find(".comment-header-user", first=True).text
        db.add_entry(user, game, rating_score)
        all_rating_scores.append((user, rating_score))
    if not "?pageid=" in game_url.split('/')[-1]:
        game_url += "?pageid=1"
    print("Page {0} of game {1}".format(game_url.split('=')[-1], game))
    game_url = game_url[:-1] + str(int(game_url[-1]) + 1)
    # Go to number of matches
    match_text = soup.find(".ng-isolate-scope")[56].text.replace(',', '').split(' of ')
    print(match_text)
    # Check to see if at last page
    number_matches = match_text[1].split(' ')[0]
    if match_text[0][-len(number_matches):] == number_matches:
        return None
    return game_url


def parse_all_ratings(game_url):
    if not 'ratings' in game_url.split('/')[-1]:
        game_url += '/ratings'
    game = game_url.split('/')[-2]
    if not db.game_completed(game):
        while game_url:
            game_url = parse_ratings(game_url)




def test():
    db.mark_game_completed('dominion')
    url = test_bg_ratings
    parse_all_ratings(url)
    print(db.get_entries_by_game("dominion"))


if __name__ == '__main__':
    test()
