from flask import *
from src import Anime
import os
from time import time
from requests import get
# mulai
app = Flask(__name__)

@app.route('/api/anime', methods=['GET', 'POST'])
def anim():
    if request.args.get('id') and request.args.get('q'):
      return {
        'status': False,
        'error': 'Input just One parameter'
      }
    elif request.args.get('q'):
        start=time()
        anime = Anime(request.args.get('q'))
        end = time()
        return {
            "type": anime.type,
            "status": anime.status,
            "episode": anime.episode,
            "aired": anime.aired,
            "broadcast": anime.broadcast,
            "premiered": anime.primer,
            "licensors": anime.licencors,
            "studio": anime.studio,
            "producers": anime.producers,
            "source": anime.source,
            "score": anime.score,
            "duration": anime.duration,
            "ranked": anime.ranked,
            "rating": anime.rating,
            "genre": anime.genre,
            "popular": anime.popular,
            "member": anime.member,
            "favorites": anime.favorites,
            "title": anime.orititle,
            'related': {
                'adaptation': anime.adaptation,
                'prequel': anime.prequel,
                'sequel': anime.sequel,
                'side story': anime.side,
                'alternative version': anime.alterver,
                'other': anime.other
            },
            'time': end-start,
            'url': anime.url,
            'airing': anime.airing,
            'nsfw': anime.nsfw,
            'id': anime.id,
            'theme': anime.theme,
            'demographic': anime.demographic,
            'description': anime.description,
            'jp_title': anime.jp_title,
            'en_title': anime.en_title,
            'synonyms': anime.syn_title,
            'image_url': anime.img_url,
            'trailer_url':anime.pv
        }
    elif request.args.get('id'):
      if get(f"https://myanimelist.net/anime/{request.args.get('id')}/").status_code == 404:
        return {
          'status': False,
          'error': 'Invalid ID'
        }
      else:
        pass
      start=time()
      anime = Anime(mal_id=request.args.get('id'))
      end=time()
      return {
            "type": anime.type,
            "status": anime.status,
            "episode": anime.episode,
            "aired": anime.aired,
            "broadcast": anime.broadcast,
            "premiered": anime.primer,
            "licensors": anime.licencors,
            "studio": anime.studio,
            "producers": anime.producers,
            "source": anime.source,
            "score": anime.score,
            "duration": anime.duration,
            "ranked": anime.ranked,
            "rating": anime.rating,
            "genre": anime.genre,
            "popular": anime.popular,
            "member": anime.member,
            "favorites": anime.favorites,
            "title": anime.orititle,
            'related': {
                'adaptation': anime.adaptation,
                'prequel': anime.prequel,
                'sequel': anime.sequel,
                'side story': anime.side,
                'alternative version': anime.alterver,
                'other': anime.other
            },
            'time': end-start,
            'url': anime.url,
            'airing': anime.airing,
            'nsfw': anime.nsfw,
            'id': anime.id,
            'theme': anime.theme,
            'demographic': anime.demographic,
            'description': anime.description,
            'jp_title': anime.jp_title,
            'en_title': anime.en_title,
            'synonyms': anime.syn_title,
            'image_url': anime.img_url,
            'trailer_url':anime.pv
        }
    
    else:
        return {
            "status": False,
            "error": "Input parameter q"
        }
@app.errorhandler(404)
def error(e):
	return {
        "status": 404
    }
@app.route('/', methods=['GET', 'POST'])
def api():
    return {
        "msg": "Welcome to myanimelist unofficial api",
        "author": "Babwa Wibu"
    }

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
