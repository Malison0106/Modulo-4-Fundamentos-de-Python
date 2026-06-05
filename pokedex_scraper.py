import requests as req
import timeit
import time
import pandas as pd
from IPython.display import Image, HTML
import random
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry
 
 
 
## Rate limit to help with overcalling
## pokemon api is 100 calls per 60 seconds max
@sleep_and_retry
@limits(calls=1000, period=60)
def call_api (url) :
    response = req.get(url)
 
    if response.status_code == 404 :
        return 'Not Found'
    if response.status_code != 200 :
        print( 'here' , response.status_code, url)
        raise Exception( 'API response: {}' .format(response.status_code))
    return response
 
 
API_POKEMON = 'https://pokeapi.co/api/v2/pokemon/{pokemon}'
 
def get_number_pokemon () :
    res = req.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=898')
    pokemon_links_values = [link[ 'url' ] for link in res.json()[ 'results' ]]
    return pokemon_links_values
 
def get_pokemon (link= '' ) :
    
    info = None
    resolved = False
    retries = 0
    max_retries = 3
    
    try :
        while not resolved and retries < max_retries:
            
            res = None
            tooManyCalls = False
 
            try :
                res = call_api(link)
                if res == 'Not Found' :
                    resolved = True
                    break
            except Exception as e:
                print(f"Error en call_api: {e}")
                retries += 1
                if retries < max_retries:
                    time.sleep(2)
                    continue
                else:
                    break
                    
            if res and res.status_code < 300 :
 
                pokemon_info = res.json()
 
                info = {
                    'Image' : pokemon_info.get('sprites', {}).get('front_default'),
                    'id' : pokemon_info.get('id'),
                    'name' : pokemon_info.get('name'),
                    'height' : pokemon_info.get('height'),
                    'base_experience' : pokemon_info.get('base_experience'),
                    'weight' : pokemon_info.get('weight'),
                    'species' : pokemon_info.get('species', {}).get('name')
 
                }
 
                resolved = True
 
            elif res and res.status_code == 429 :
                time.sleep(2)
            elif res:
                sleep_val = 1
                time.sleep(sleep_val)
                retries += 1
                
    except Exception as e:
        print(f"Error general en get_pokemon: {e}")
        return info
    finally :
        return info
            
 
 
 
def get_all_pokemon (links_pokemon=None) :
    
    
    list_pokemon = []
    for link in tqdm(links_pokemon):
        
        pokemon = get_pokemon(link)
        if pokemon != None :
            list_pokemon.append(pokemon)
        time.sleep( 0.1 )
        
            
    pd.set_option( 'display.max_colwidth' , None )
 
    df_pokemon = pd.DataFrame(list_pokemon)
      
    return df_pokemon
    
 
def image_formatter (im) :
    return f'<img src=" {im} ">'
 
def main_pokemon_run () :
    links_pokemon = get_number_pokemon()
    print(f"Se obtuvieron {len(links_pokemon)} Pokémon")
 
    df_pokemon = get_all_pokemon(links_pokemon=links_pokemon)
    print(f"Se descargaron datos de {len(df_pokemon)} Pokémon")
    
    df_pokemon.sort_values([ 'id' ],inplace= True )
    return df_pokemon, HTML(df_pokemon.iloc[ 0 : 4 ].to_html(formatters={ 'Image' : image_formatter}, escape= False ))


# Ejecutar si se corre directamente
if __name__ == '__main__':
    try:
        df, html_display = main_pokemon_run()
        print("\n=== Primeros 4 Pokémon ===")
        print(df.iloc[0:4][['id', 'name', 'height', 'weight']])
    except Exception as e:
        print(f"Error ejecutando main: {e}")
        import traceback
        traceback.print_exc()
