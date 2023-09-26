from bs4 import BeautifulSoup
import requests
import re


class MetaSput:

    # def __init__(self, year):
    #     self.year = year

    def sputnik(self, year):

        sputnik_base = f"https://www.sputnikmusic.com/best/albums/{year}/"

        headers = {
            "User-Agent": "Defined",
            "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9"
        }

        sputnik_ = (requests.get(sputnik_base, headers=headers, allow_redirects=False)).text
        sputnik_soup = BeautifulSoup(sputnik_, 'html.parser')

        sput_artist_uncleaned = sputnik_soup.select('b')
        sput_artist = []

        for item in sput_artist_uncleaned[::2]:
            item = item.text
            sput_artist.append(item)

        sput_album_uncleaned = sputnik_soup.find_all("font", class_='darktext')
        sput_album = []

        for item in sput_album_uncleaned:
            item = item.text
            sput_album.append(item)

        return sput_artist, sput_album

    def metacritic(self, year):

        page = 0
        lowest_score = 100
        meta_artist_name = []
        meta_album_name = []
        while lowest_score > 74:
            metacritic_base = f"https://www.metacritic.com/browse/albums/score/metascore/year/filtered?view=condensed&" \
                              f"year_selected={year}&sort=desc&page={page}"

            headers = {
                "User-Agent": "Defined",
                "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                          "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
            metacritic_text = (requests.get(metacritic_base, headers=headers, allow_redirects=False)).text
            meta_soup = BeautifulSoup(metacritic_text, 'html.parser')
            meta_score = []
            meta_score_num = meta_soup.select("div.metascore_w.large.release.positive")
            meta_album_uncleaned = meta_soup.select("a h3")
            meta_artist_uncleaned = meta_soup.find_all("div", class_="artist")

            for item in meta_score_num:
                if '.' in str(item):
                    pass
                else:
                    item = re.findall(r'\d+', str(item))
                    meta_score.append(int(item[0]))
            counter = 0
            for score, album, artist in zip(meta_score, meta_album_uncleaned, meta_artist_uncleaned):

                if score < 75:
                    lowest_score = 74
                    break
                else:
                    album = album.text
                    meta_album_name.append(str(album))
                    artist = artist.text
                    artist = artist[36:].strip()
                    meta_artist_name.append(str(artist))

                counter += 1
            page += 1
        return meta_artist_name, meta_album_name

    def combined_list(self, sputnik, metacritic):

        combined_artists = []
        combined_albums = []
        metacritic_artists, metacritic_albums = metacritic
        sputnik_artist, sputnik_album = sputnik

        for item in sputnik_artist:
            combined_artists.append(item)
        for item in sputnik_album:
            combined_albums.append(item)
        for item in metacritic_artists:
            combined_artists.append(item)
        for item in metacritic_albums:
            combined_albums.append(item)

        return combined_albums, combined_artists

