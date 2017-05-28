import requests
from bs4 import BeautifulSoup
from collections import namedtuple


Film = namedtuple('Film', 'name,number_theatres,afisha_rate,afisha_number_rates')


def fetch_afisha_page():
    url = 'https://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(url).content


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    movies_rows_bundle = soup.find('div', attrs={
        'class': 'b-theme-schedule m-schedule-with-collapse',
        'id': 'schedule',
    }).find_all('div', attrs={
        'class': 'object s-votes-hover-area collapsed'
    })
    for movie in movies_rows_bundle:
        afisha_movie_id = movie.attrs['id'].split('_')[-1]
        afisha_movie_title = movie.find('div', attrs={'class': 'm-disp-table'}).find(
            'h3', attrs={'class': 'usetags'}).find('a').text
        afisha_theatre_count = _get_theatre_count(afisha_movie_id)


def _get_theatre_count(afisha_movie_id):
    url = 'https://www.afisha.ru/msk/schedule_cinema_product/{}/'.format(afisha_movie_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')


def fetch_movie_info(movie_title):
    return 42


def output_movies_to_console(movies):
    for movie in sorted(movies, key=lambda x: x):
        print('{movie.title}\t{movie.rating}\t{movie.rating_count}\t'.format(movie))


if __name__ == '__main__':
    afisha_html = fetch_afisha_page()
    movies = parse_afisha_list(afisha_html)
    output_movies_to_console(movies)
