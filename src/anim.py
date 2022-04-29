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

def func_list(func: str, attrName='title', attrId: int=3):
    hasil = []
    a = 0
    try:
        for i in func:
            hasil.append({'url': 'https://myanimelist.net{}'.format(i['href']), attrName: i.text, 'id': i['href'].split('/')[attrId], 'type': i['href'].split('/')[1]})
            a += 1
    except: pass
    return hasil
def tagg(tag: str, value, soup):
    try:
        return soup.find(tag, string=value).parent.find_all('a')
    except:
        return []
class Anime():
    def __init__(self, title: str = None, mal_id = None):
        s = requests.Session()
        s.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                })
        headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
        if mal_id == None:
          url = 'https://www.bing.com/search?q=myanimelist.net/anime+{}&setlang=en-us'.format(title)
          res = requests.get(url, headers=headers).text
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
        
        licensors= ListSoupFind('Licensors:', soup)
        type = re.search(r'<a href="https://myanimelist.net/topanime.php\?type\=(.*?)"', soup.prettify()).group(1).upper()
        orititle = soup.strong.text
        score = soup.find('span', string='Score:').next_sibling.next_sibling.text
        studio = ListSoupFind('Studios:', soup)

        #Related anime
        adaptation = func_list(tagg('td', 'Adaptation:', soup), attrId=2)
        side = func_list(tagg('td', 'Side story:', soup), attrId=2)
        prequel = func_list(tagg('td', 'Prequel:', soup), attrId=2)
        alterver = func_list(tagg('td','Alternative version:', soup), attrId=2)
        other = func_list(tagg('td','Other:', soup), attrId=2)
        sequel = func_list(tagg('td','Sequel:', soup), attrId=2)
        
        if not studio:
            studio = StrFind('Studio:', soup)
        producers = func_list(tagg('span', 'Producers:', soup), 'name')
        source = StrFind('Source:', soup)
        try: genres = func_list(tagg('span','Genres:', soup), 'name')
        except: genres = func_list(tagg('span','Genre:', soup), 'name')
        try: theme = func_list(tagg('span','Theme:', soup), 'name')
        except: theme = 'None'
        try: demographic = func_list(tagg('span','Demographic:', soup), 'name')
        except: demographic = 'None'
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

