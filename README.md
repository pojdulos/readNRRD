readNRRD
========

konwertuje dane wolumetryczne z bazy PDDCA w formacie .nrrd do postaci akceptowalnej przez Detectron

Program w oparciu o zawartość pliku img.nrrd generuje pliki graficzne (domyślnie .jpg) oraz tworzy plik opisu via_region_data.json

UWAGA
-----

W obecnej wersji opis jest tworzony tylko dla wysegmentowanej żuchwy (z pliku Mandible.nrrd).

PRZED UŻYCIEM
-------------

W celu użycia należy zmodyfikować w źródle stałe: SRC_ROOT oraz DST_ROOT według swoich potrzeb
