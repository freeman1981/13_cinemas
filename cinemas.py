import requests
from lxml import etree
from bs4 import BeautifulSoup
from collections import namedtuple


Film = namedtuple('Film', 'title,theatres_count,rate,rate_count')


def fetch_afisha_page():
    list_movies_in_afisha_url = 'https://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(list_movies_in_afisha_url).content


def parse_afisha_list(raw_html):
    parsed_afisha_list = []
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
        rating_ball, rating_count = fetch_movie_info(afisha_movie_title)
        parsed_afisha_list.append(Film(
            title=afisha_movie_title,
            theatres_count=afisha_theatre_count,
            rate=rating_ball,
            rate_count=rating_count,
        ))
    return parsed_afisha_list


def _get_theatre_count(afisha_movie_id):
    theatre_info_url = 'https://www.afisha.ru/msk/schedule_cinema_product/{}/'.format(afisha_movie_id)
    response = requests.get(theatre_info_url)
    soup = BeautifulSoup(response.content, 'lxml')
    table_shedule_all_rows = soup.find('div', attrs={'class': 'b-theme-schedule'}).select('div table a[href]')
    return len([item for item in table_shedule_all_rows if item.attrs['href'] != '#'])


def fetch_movie_info(movie_title):
    search_in_kinopoisk_url = 'https://www.kinopoisk.ru/index.php'
    params = {
        'kp_query': movie_title
    }
    response = requests.get(search_in_kinopoisk_url, params)
    soup = BeautifulSoup(response.content, 'lxml')
    kinopoisk_movie_id = soup.find('div', attrs={'class': 'element most_wanted'}).find(
        'div', attrs={'class': 'info'}).find('p', attrs={'class': 'name'}).select_one('a[href]').attrs['data-id']
    rating_kinopoisk_url = 'https://rating.kinopoisk.ru/{}.xml'.format(kinopoisk_movie_id)
    response = requests.get(rating_kinopoisk_url)
    kp_rating_tag = etree.fromstring(response.content).xpath('kp_rating')[0]
    rating_ball = kp_rating_tag.text
    rating_count = kp_rating_tag.attrib['num_vote']
    return rating_ball, rating_count


def output_movies_to_console(movies):
    for movie in sorted(movies, key=lambda x: x):
        print('{movie.title}\t{movie.rating}\t{movie.rating_count}\n'.format(movie))


if __name__ == '__main__':
    afisha_html = fetch_afisha_page()
    movies = parse_afisha_list(afisha_html)
    output_movies_to_console(movies)
