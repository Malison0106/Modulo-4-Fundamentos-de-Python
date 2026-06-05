# Importar librerías necesarias
import requests as req
import timeit
import time
import pandas as pd
from IPython.display import Image, HTML
import random
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry

# Decorador para controlar la velocidad de llamadas a la API
@sleep_and_retry
@limits(calls=1000, period=60)
def call_api (url) :
    response = req.get(url)
    
    if response.status_code == 404 :
        return 'Not Found'
    if response.status_code != 200 :
        print( 'Error' , response.status_code, url)
        raise Exception( 'API response: {}' .format(response.status_code))
    return response
 
 
# URL base de la API
API_POKEMON = 'https://pokeapi.co/api/v2/pokemon/{pokemon}'

# Obtener lista de todos los Pokémon
def get_number_pokemon () :
    res = req.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=898')
    pokemon_links_values = [link[ 'url' ] for link in res.json()[ 'results' ]]
    return pokemon_links_values
 
# Descargar información de un Pokémon
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
                print(f"Error: {e}")
                retries += 1
                if retries < max_retries:
                    time.sleep(2)
                    continue
                else:
                    break
                    
            if res and res.status_code < 300 :
                pokemon_info = res.json()
                
                # Extraer datos del Pokémon
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
        print(f"Error: {e}")
        return info
    finally :
        return info
            

# Descargar todos los Pokémon
def get_all_pokemon (links_pokemon=None) :
    list_pokemon = []
    
    # Descargar cada Pokémon con barra de progreso
    for link in tqdm(links_pokemon):
        pokemon = get_pokemon(link)
        if pokemon != None :
            list_pokemon.append(pokemon)
        time.sleep( 0.1 )
        
    # Convertir a DataFrame
    pd.set_option( 'display.max_colwidth' , None )
    df_pokemon = pd.DataFrame(list_pokemon)
      
    return df_pokemon
    
# Formatear imagen para mostrar en HTML
def image_formatter (im) :
    return f'<img src=" {im} ">'

# Función principal que ejecuta todo
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
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
