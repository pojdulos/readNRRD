readNRRD
========

konwertuje dane wolumetryczne z bazy PDDCA w formacie .nrrd do postaci
akceptowalnej przez Detectron

Program w oparciu o zawartość pliku img.nrrd generuje pliki graficzne
(domyślnie .jpg) oraz tworzy plik opisu via_region_data.json

PRZED UŻYCIEM
-------------

Aby ustawić poprawne scieżki dostępu należy w pliku consts.py zmodyfikować
stałe SRC_ROOT oraz DST_ROOT według swoich potrzeb.

Opis jest tworzony tylko dla jednej wysegmentowanej struktury
(domyślnie żuchwy: 'Mandible'). Można wybrać inna strukturę modyfikując
w pliku consts.py stałą SEGMENTED_STRUCTURE. Należy jej przypisać nazwę
odpowiedniego pliku z katalogu structures bez rozszerzenia.
