from pathlib import Path

# Insira aqui o diretório da sua pasta principal (gamma)
PROJ_PATH_LIST = ['C:/Users/55249/Documents/GitHub/LinkedIn-scrap/jobsearch',
                  'your path adrdress here']

found_path = False
for path in PROJ_PATH_LIST:
    if Path(path).exists():
        PROJ_PATH  = Path(path)
        found_path = True

if not(found_path):
    PROJ_PATH = Path.cwd().parents[1]
    
DATA_PATH_RAW     = PROJ_PATH / 'data' / 'raw'
DATA_PATH_WRANGLE  = PROJ_PATH / 'data' / 'wrangle'
DATA_PATH_RESULTS = PROJ_PATH / 'data' / 'results'
DATA_PATH_FILES   = PROJ_PATH / 'files'