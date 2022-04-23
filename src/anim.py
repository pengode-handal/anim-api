import requests, re
from bs4 import BeautifulSoup as bs

def SoupFind(value, soup):
    return soup.find("span", string=value)
def ListSoupFind(value, soup):
  try:
    if 'None' in SoupFind(value, soup).parent.text:
      return []
    else:
      return SoupFind(value, soup).parent.text.replace('      ', '').replace('\n', ',').split(',')[2:]
  except:
    return []
def StrFind(value, soup):
  try:
    return SoupFind(value, soup).next_sibling.strip()
  except:
    return 'Unknown'
def ListInUrl(value, soup):
    return soup.find()
def related_list(func):
    atype, idnim, title, url, hasil = [], [], [], [], []
    a = 0
    try:
        for i in func:
            a += 1
            if 'manga' in func[a-1]:
                atype.append('manga')
                idnim.append(re.search(r'href\="\/manga\/(.*?)\/', func[a-1]).group(1))
                title.append(re.search(r'">(.*?)</a>', func[a-1]).group(1))
                url.append('https://myanimelist.net'+re.search(r'href\=\"(.*?)">', func[a-1]).group(1))
                hasil.append({'url': url[a-1], 'title': title[a-1], 'id': idnim[a-1], 'type': atype[a-1]})
            elif 'anime' in func[a-1]:
                atype.append('anime')
                idnim.append(re.search(r'href\="\/anime\/(.*?)\/', func[a-1]).group(1))
                title.append(re.search(r'">(.*?)</a>', func[a-1]).group(1))
                url.append('https://myanimelist.net'+re.search(r'href\=\"(.*?)">', func[a-1]).group(1))
                hasil.append({'url': url[a-1], 'title': title[a-1], 'id': idnim[a-1], 'type': atype[a-1]})
    except:
        hasil = []
    return hasil
def genre_list(func: str):
    atype, idnim, name, url, hasil = [], [], [], [], []
    a = 0
    try:
        for i in func:
            a += 1
            if 'manga' in func[a-1]:
                atype.append('manga')
                idnim.append(re.search(r'href\="\/manga\/genre\/(.*?)\/', func[a-1]).group(1))
                name.append(re.search(r'title\="(.*?)"', func[a-1]).group(1))
                url.append('https://myanimelist.net'+re.search(r'href\=\"(.*?)" ti', func[a-1]).group(1))
                hasil.append({'url': url[a-1], 'name': name[a-1], 'id': idnim[a-1], 'type': atype[a-1]})
            elif 'anime' in func[a-1]:
                atype.append('anime')
                idnim.append(re.search(r'href\="\/anime\/genre\/(.*?)\/', func[a-1]).group(1))
                name.append(re.search(r'title\="(.*?)"', func[a-1]).group(1))
                url.append('https://myanimelist.net'+re.search(r'href\=\"(.*?)\" ti', func[a-1]).group(1))
                hasil.append({'url': url[a-1], 'name': name[a-1], 'id': idnim[a-1], 'type': atype[a-1]})
    except:
        hasil = []
    return hasil
def related(value, soup):
    try:
        return str(soup.find('td', string=value).next_element.next_element).split('<a')[1:]
    except:
        return []
class Anime():
    def __init__(self, title: str = None, mal_id = None):
        s = requests.Session()
        s.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                })
        if mal_id == None:
          url = 'https://duckduckgo.com/?q=site%3Amyanimelist.net/anime+{}'.format(title)
          res = s.get(url).text
          try: URL = 'https://myanimelist.net/anime/' + re.search(r'href="https://myanimelist.net/anime/(.*?)"', res).group(1)
          except:
            print(res)
        elif title == None:
          URL = f'https://myanimelist.net/anime/{mal_id}'
        id = re.search(r'anime/(\d+)', URL).group(1)
        soup = bs(s.get(URL).text, 'html.parser')
        episodes = soup.find('span', string='Episodes:').next_sibling.strip()
        status = soup.find('span', string='Status:').next_sibling.strip()
        aired = soup.find('span', string='Aired:').next_sibling.strip()
        broadcast = StrFind('Broadcast:', soup)
        try: 
          primer = soup.find('span', string='Premiered:').next_sibling.next_sibling.text 
        except:
          primer = 'Unknown'
        sequel = ListSoupFind('Sequel', soup)
        licensors= ListSoupFind('Licensors:', soup)
        type = re.search(r'<a href="https://myanimelist.net/topanime.php\?type\=(.*?)"', soup.prettify()).group(1).upper()
        orititle = soup.strong.text
        score = soup.find('span', string='Score:').next_sibling.next_sibling.text
        studio = ListSoupFind('Studios:', soup)

        adaptation = related_list(related('Adaptation:', soup))
        side = related_list(related('Side story:', soup))
        prequel = related_list(related('Prequel:', soup))
        alterver = related_list(related('Alternative version:', soup))
        other = related_list(related('Other:', soup))
        sequel = related_list(related('Sequel:', soup))
        if not studio:
            studio = StrFind('Studio:', soup)
        producers = ListSoupFind('Producers:', soup)
        source = StrFind('Source:', soup)
        try:
            genres = genre_list(str(SoupFind('Genres:', soup).parent.find_all('a')).split('<a')[1:])
        except:
            genres = genre_list(str(SoupFind('Genre:', soup).parent.find_all('a')).split('<a')[1:])
        try:
            theme = genre_list(str(SoupFind('Theme:', soup).parent.find_all('a')).split('<a')[1:])
        except:
            theme = 'None'
        try:
            demographic = genre_list(str(SoupFind('Demographic:', soup).parent.find_all('a')).split('<a')[1:])
        except:
            demographic = 'None'
        try: trailer_url = "https://www.youtube.com/watch?v="+re.search(r'embed\/(.*?)\?', soup.find('a', {'class': 'iframe js-fancybox-video video-unit promotion'})['href'] ).group(1)
        except: trailer_url = 'None'
        duration = StrFind('Duration:', soup)
        rating = StrFind('Rating:', soup)
        members = StrFind('Members:', soup)
        favorites = StrFind('Favorites:', soup)
        ranked = StrFind('Ranked:', soup)
        popularity = StrFind('Popularity:', soup)
        description = soup.find("p", {"itemprop": "description"}).text
        if 'airing' in str(status).lower():
          airing = True
        else:
          airing = False
        if 'nudity' in rating or 'hentai' in rating:
          is_nsfw = True
        else:
          is_nsfw=False
        try: img_url = soup.find('img', {'itemprop': 'image'})['data-src']
        except: img_url = 'None'
        self.img_url = img_url
        self.episode = episodes
        self.status = status
        self.aired = aired
        self.broadcast = broadcast
        self.primer = primer
        self.licencors = licensors
        self.studio = studio
        self.producers = producers
        self.source = source
        self.adaptation = adaptation
        self.genre = genres
        self.duration = duration
        self.rating = rating
        self.score = score
        self.ranked = ranked
        self.popular = popularity
        self.member = members
        self.type = type
        self.favorites = favorites
        self.orititle = orititle
        self.sequel = sequel
        self.side = side
        self.prequel = prequel
        self.alterver = alterver
        self.other = other
        self.url = URL
        self.airing = airing
        self.nsfw = is_nsfw
        self.id = id
        self.demographic = demographic
        self.theme = theme
        self.description = description
        self.pv = trailer_url or None
        self.jp_title = StrFind('Japanese:', soup)
        self.en_title = StrFind('English:', soup)
        self.syn_title = StrFind('Synonyms:', soup)

