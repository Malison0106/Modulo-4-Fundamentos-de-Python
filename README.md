# Pokémon Data Scraper - PokeAPI

## Descripción

Este proyecto utiliza la **PokeAPI** para descargar información de todos los Pokémon disponibles y organizarla en un **DataFrame de Pandas**. El objetivo es facilitar el análisis y la visualización de datos de Pokémon en entornos como Jupyter Notebook.

## Características

- 📥 **Descarga automática**: Obtiene datos de los 898 Pokémon (desde Bulbasaur hasta Calyrex)
- 🔄 **Rate Limiting**: Respeta los límites de la API con control de velocidad
- 🐼 **DataFrame Pandas**: Organiza los datos en una estructura tabular para análisis
- 📊 **Información completa**: Incluye ID, nombre, altura, peso, experiencia base, especie e imagen
- 🔁 **Reintentos automáticos**: Manejo robusto de errores con reintentos
- ⚡ **Optimizado**: Delay configurable entre llamadas para máximo rendimiento

## Requisitos

- Python 3.7+
- `requests`: Para hacer llamadas HTTP a la API
- `pandas`: Para manipulación de datos
- `tqdm`: Para barras de progreso
- `ratelimit`: Para control de frecuencia de llamadas

## Instalación

```bash
pip install requests pandas tqdm ratelimit
```

## Uso

### Como Script Directo

```python
python pokedex_scraper.py
```

Esto ejecutará la simulación completa y mostrará los primeros 4 Pokémon con su información.

### En Jupyter Notebook

```python
from pokedex_scraper import main_pokemon_run

df, html_display = main_pokemon_run()
print(df.head(10))
display(html_display)
```

### Funciones Disponibles

#### `get_number_pokemon()`
Obtiene la lista de URLs de los 898 Pokémon desde la PokeAPI.

#### `get_pokemon(link)`
Descarga información individual de un Pokémon dado su URL.

#### `get_all_pokemon(links_pokemon)`
Procesa múltiples Pokémon en paralelo usando `tqdm` para mostrar progreso.

#### `main_pokemon_run()`
Ejecuta la simulación completa y retorna un DataFrame con todos los datos.

## Estructura de Datos

El DataFrame contiene las siguientes columnas:

| Columna | Descripción |
|---------|------------|
| `id` | Número de Pokédex (1-898) |
| `name` | Nombre del Pokémon |
| `height` | Altura en decímetros |
| `weight` | Peso en hectogramos |
| `base_experience` | Experiencia base |
| `species` | Especie/Tipo del Pokémon |
| `Image` | URL de la imagen del Pokémon |

## Tiempo de Ejecución

- Primera descarga: **15-30 minutos** (depende de tu conexión)
- Ejecuciones posteriores: Casi instantáneo (con cache)

## API Utilizada

- **PokeAPI v2**: https://pokeapi.co/api/v2/
- Límite: 100-300 llamadas por minuto (configurado en el código)

## Notas Importantes

- La API de Pokémon es pública y gratuita
- Respetar los límites de rate limiting es importante
- El primer tiempo de ejecución es lento debido a la descarga de ~900 Pokémon
- Los datos se cachean en memoria durante la sesión

## Autor

Desarrollado como parte del módulo 4 de Fundamentos de Python
