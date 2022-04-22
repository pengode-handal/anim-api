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
    return None
def ListInUrl(value, soup):
    return SoupFind(value, soup)
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
def related(value, soup):
    try:
        return str(soup.find('td', string=value).next_element.next_element).split('<a')[1:]
    except:
        return []
class Anime():
    def __init__(self, title: str = None, mal_id = None):
        s = requests.Session()
        s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
        s.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'referer':'https://www.google.com/'
                })
        if mal_id == None:
          url = 'https://www.bing.com/search?q=myanimelist.net%2B{}+anime'.format(title)
          res = s.get(url).text
          URL = 'https://myanimelist.net/anime/' + re.search(r'<a href="https://myanimelist.net/anime/(.*?)"', res).group(1)
        elif title == None:
          URL = f'https://myanimelist.net/anime/{mal_id}'
        soup = bs(s.get(URL).text, 'html.parser')
        episodes = soup.find('span', string='Episodes:').next_sibling.strip()
        status = soup.find('span', string='Status:').next_sibling.strip()
        aired = soup.find('span', string='Aired:').next_sibling.strip()
        broadcast = StrFind('Broadcast:', soup)
        try: 
          primer = soup.find('span', string='Premiered:').next_sibling.next_sibling.text 
        except:
          primer = None
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
        genres = ListSoupFind('Genres:', soup)
        if not genres:
            genres = ListSoupFind('Genre:',soup)
        duration = StrFind('Duration:', soup)
        rating = StrFind('Rating:', soup)
        members = StrFind('Members:', soup)
        favorites = StrFind('Favorites:', soup)
        ranked = StrFind('Ranked:', soup)
        popularity = StrFind('Popularity:', soup)
        if 'Finished' in status:
          airing = False
        else:
          airing = True
        if 'Mild' in rating:
          is_nsfw = True
        else:
          is_nsfw=False
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
