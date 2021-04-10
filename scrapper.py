"""
This file scrapes the bgg website for user ratings
"""
# imports
# from bs4 import BeautifulSoup
# import requests
from requests_html import HTMLSession

# constants
test_bg = "https://boardgamegeek.com/boardgame/36218/dominion"
test_bg_ratings  = test_bg + '/ratings'
test_user = "https://boardgamegeek.com/user/Sacrilon"
test_user_owned = "https://boardgamegeek.com/collection/user/Sacrilon?own=1&subtype=boardgame&ff=1"


def get_soup(url):
    # Gets the parse (soup) for a given website
    session = HTMLSession()
    req = session.get(url)
    req.html.render()
    return req.html


def parse_ratings(game_url):
    soup = get_soup(game_url)
    # Get (user, rating) pairings
    all_rating_scores = list()
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
        all_rating_scores.append((user, rating_score))
    print(all_rating_scores)




def test():
    url = test_bg_ratings
    parse_ratings(url)


if __name__ == '__main__':
    test()
