# name: Ryan Oliveira
"""
Imported libraries
"""
import sys
import omdb
import requests
from bs4 import BeautifulSoup as BS

API_KEY = 'fc03d7c8'  # API Access Key
omdb.set_default('apikey', API_KEY)


class MovieData:
    """Grab a Movies technical info and trivial data.

    Parameters
    ----------
    movie_title : `str`
            title of movie that will have its data retrieved
    fullplot : `bool`
            True will retrieve full plot of movie, False will retrieve summary
    load_all_data : `bool`
            True will run all methods to grab data, False will wait for method activation

    Examples
    --------
    To create an object:
    >> movie = MovieData('The Matrix', fullplot=True, load_all_data=False)

    To retrieve movie specific movie info:
    >> object.movie_technical_info['actors']

    Notes
    -----
    movie_technical_info Options below:
    actors, awards, box_office, country, dvd,
    director, genre, language, metascore, plot,
    poster, production, rated, released, response,
    runtime, title, type, website, writer, year,
    imdb_id, imdb_rating, imdb_votes
    """
    def __init__(self, movie_title, fullplot=False,
                 load_all_data=False): # full plot and load_all_data False by default
        try:
            self.movie_technical_info = omdb.get(title=movie_title, fullplot=fullplot, tomatoes=False)
        except requests.exceptions.RequestException:
            print("ERROR: Could Not connect to url, please check connection.")
            sys.exit(1)

        self.imdb_id = self.movie_technical_info['imdb_id']
        self.trivia = []
        self.goofs = []
        self.quotes = []
        self.crazycredits = []
        if load_all_data:  # if true, loads all data for current movie
            self.get_trivia()
            self.get_goofs()
            self.get_quotes()
            self.get_crazy_credits()

    def get_trivia(self):
        """Grabs trivia about movie, stores as list"""
        try:
            trivia_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/trivia/?ref_=tt_trv_trv')
        except requests.exceptions.RequestException:
            print("ERROR: Could Not connect to url, please check connection.")
            sys.exit(1)
        trivia_soup = BS(trivia_page.content, 'lxml')
        self.trivia = [trivia_fact.get_text().lstrip() for trivia_fact in
                       trivia_soup.find_all('div', class_="sodatext")]

    def get_goofs(self):
        """Grabs goofs about movie, stores as list"""
        try:
            goof_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/goofs/?ref_=tt_trv_trv')
        except requests.exceptions.RequestException:
            print("ERROR: Could Not connect to url, please check connection.")
            sys.exit(1)
        goof_soup = BS(goof_page.content, 'lxml')
        self.goofs = [goof_fact.get_text().lstrip() for goof_fact in goof_soup.find_all('div', class_="sodatext")]

    def get_quotes(self):
        """Grabs quotes from movie, stores as list"""
        try:
            quotes_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/quotes/?ref_=tt_trv_trv')
        except requests.exceptions.RequestException:
            print("ERROR: Could Not connect to url, please check connection.")
            sys.exit(1)
        quotes_soup = BS(quotes_page.content, 'lxml')
        self.quotes = [quote.get_text().lstrip() for quote in quotes_soup.find_all('div', class_="sodatext")]

    def get_crazy_credits(self):
        """Grabs crazy credits about movie, stores as list"""
        try:
            crazycredits_page = requests.get(
                'http://www.imdb.com/title/' + self.imdb_id + '/crazycredits/?ref_=tt_trv_trv')
        except requests.exceptions.RequestException:
            print("ERROR: Could Not connect to url, please check connection.")
            sys.exit(1)
        crazycredits_page_soup = BS(crazycredits_page.content, 'lxml')
        self.crazycredits = [crazycredits.get_text().lstrip() for crazycredits in
                             crazycredits_page_soup.find_all('div', class_="sodatext")]
