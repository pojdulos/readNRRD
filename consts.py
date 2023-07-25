SRC_ROOT = '/home/mateusz/Desktop/readNRRD/data'
DST_ROOT = '/home/mateusz/Desktop/readNRRD/data_prp'

SEGMENTED_STRUCTURE = 'Mandible'

# True  - tworzy oddzielny podkatalog dla każdego modelu z własnym plikiem via_region_data.json
# False - zapisuje wszystko jak leci do DST_ROOT i tworzy jeden wspólny plik via_region_data.json
SEPARATE_SAMPLES = True

IMG_FORMAT = '.jpg' # mozna zapisywac do dowolnego formatu obsługiwanego przez cv2.imwrite()

REGION_DATA_FILE = 'via_region_data.json'

TRANSPOSE = True

AXES = [(0, 1, 2), (1, 0, 2), (2, 0, 1)]