# PAD - projekt finalny _Coffee varieties_
<!-- TOC -->
* [PAD - projekt finalny _Coffee varieties_](#pad---projekt-finalny-_coffee-varieties_)
  * [Opis projektu:](#opis-projektu)
  * [Źródła danych:](#źródła-danych)
  * [Struktura projektu:](#struktura-projektu)
    * [W katalogu domowym projektu:](#w-katalogu-domowym-projektu)
    * [data](#data)
  * [src](#src)
  * [Instrukcja uruchomienia:](#instrukcja-uruchomienia)
  * [Dashboard:](#dashboard)
  * [Uwagi dodatkowe:](#uwagi-dodatkowe)
<!-- TOC -->
## Opis projektu:

Projekt omawia odmiany botaniczne oraz ich różne właściwości związane z odpornością na choroby,
miejscem uprawy czy wydajnością uprawy. W ramach projektu stworzona została baza przykładowych kaw, a także model
Random Forest dobierający odmianę do danych podanych przez farmera. Analizę oraz model można obejrzeć w dasboardzie 
stworzonym w `streamlit`.

## Źródła danych:

1. Dataset wykorzystywany w projekcie powstał dzięki webscrappingowi.
2. Dataset łączy dane z dwóch źródeł.
3. W obu przypadkach pliki `robots.txt` został sprawdzony.
4. Aby uszanować serwery, między zapytaniami dodany został sleep.
5. Źródłem danych o odmianach botanicznych kawy była strona [Word Coffee Research](https://varieties.worldcoffeeresearch.org).
6. Bazę przykładów kaw uzyskałem z polskiego sklepu [CoffeeLove](https://coffeelove.pl).

## Struktura projektu:

### W katalogu domowym projektu:
1. `README.md` -> opis projektu
2. `requirements.txt` -> biblioteki potrzebne do uruchomienia projektu.

### data
Folder data zawiera dane w trzech stanach ich przetwarzania
1. `01_raw` -> zawiera pliki po webscrappingu:
- `coffee_love_corrected.tsv` -> dane z `coffeelove_data.tsv` po poprawce formatu
- `coffeelove_data.tsv` -> dane zebrane z CoffeeLove
- `varieties.tsv` -> dane zebrane z World Coffee Research

2. `02_intermediate` -> zawiera pliki po czyszczeniu:
- `cleaned_varieties.tsv` - `varieties.tsv` po usunięciu zbędnych kolumn, nadprogramowych informacji 
oraz dodaniu odmiany Heirloom jako zgrupowanej nazwy dla odmian z Ethiopii
- `coffee_love_corrected.tsv`- `coffee_love_corrected.tsv` z `01_raw` po oczyszczeniu danych 
oraz zmapowaniu wartości brakujących

3. `03_final` -> zawiera jeden plik - `merged_files.tsv`, który jest połączeniem plików z `02_intermediate`

## src
Folder src zawiera wszystkie skrypty py użyte w projekcie, a także model i jego metryki, poukładane w podfoldery:
1. `Dashboard` zawiera jeden plik -> `streamlit_dashboard.py`, jest to skrypt napisany w bibliotece `streamlit`.
Zawiera dasboard. Instrukcja uruchomienia znajduję się w odpowiedniej sekcji poniżej.
2. `DataAnalysis` zawiera jeden plik -> `data_analysis.py`, w którym znajdują się metody, dzięki którym 
`streamlit_dashboard.py` wyświetla analizy datasetu.
3. `DataProcessing` - zawiera skrypty związane z przetwarzaniem i czyszczeniem danych:
- folder `utils` zawiera stałe potrzebne do obróbki pliku `data/01_raw/coffee_love_corrected.tsv`
- `01_analyze_coffee_love_for_cleaning.py` zawiera metody, których używałem do analizy zawartości pliku 
`data/01_raw/coffee_love_corrected.tsv` w celu jego obróbki i re-anotacji
- `02_clean_coffee_love.py` wykorzystuje obserwacje z pliku powyżej oraz plik z `utils` do obróbki i re-anotacji 
`data/01_raw/coffee_love_corrected.tsv`. W jego wyniku powstaje plik `data/02_intermediate/coffee_love_corrected.tsv`
- `03_clean_varities.py` skrypt, który pozwala na usunięcie zbędnych kolumn i nadprogramowych informacji 
oraz dodanie odmiany Heirloom jako zgrupowanej nazwy dla odmian z Ethiopii. W jego wyniku powstaje plik `data/02_intermediate/cleaned_varieties.tsv` 
- `04_merge_files.py` łączy pliki z `data/02_intermediate` w ostateczny dataset `data/03_final/merged_files.tsv`
4. `ModelTraining` to folder zawierający pliki związane z trenowanie modelu Random Forest
- `label_encoders.pkl` -> zawiera zakodowane wartości potrzebne do używania modelu
- `metrics.tsv` -> zawiera metryki dla modelu z `train_random_forest.py`, powstaje w jego wyniku
- `model_interface.py` -> zawiera metody dzięki którym `src/Dashboard/streamlit_dashboard.py` moze korzystać z modelu
- `random_forest_model.pkl` -> zawiera wytrenowany model
- `train_random_forest.py` -> zawiera trening RandomForest na pliku 
`data/03_final/merged_files.tsv` do klasyfikacji odmian botanicznych kawy
5. `WebScrapping` zawiera skrypty, dzięki który scrappowane są dane z internetu
- `coffelove_web_scrapping.py` to skrypt, który zbiera dane z CoffeeLove i zapisuje je do `dane/01_raw/coffeelove_data.tsv`
- `correct_coffee_love_file.py` to skrypt, który poprawia format zapisu pliku ze skryptu powyżej i zapisuje go do `dane/01_raw/coffee_love_corrected.tsv.tsv`
- `varities_web_scrapping.py` to skrypt, który zbiera dane z WorldCoffeeResearch i zapisuje je do `dane/01_raw/varieties.tsv`

## Instrukcja uruchomienia:

1. Projekt powstał przy użyciu Python'a 3.10.
2. Potrzebne biblioteki znajdują się w pliku `requirements.txt`.
3. Aby zainstalować potrzebne biblioteki, należy z katalogu projektu uruchomić:

```
pip install -r requirements.txt
```

4. Skrypty niezwiązane ze streamlitem można uruchamiać normalnie to jest na przykład poprzez `run` w IDE.

## Dashboard:

1. Dashboard korzysta ze `streamlita`
2. Streamlit jest niezwykle wyczulony na ścieżki. W związku z tym należy uruchamiać go z katalogu głównego projektu.
3. Aby uruchomić dashboard należy użyć komendy:
```
streamlit run src/Dashboard/streamlit_dashboard.py
```
**UWAGA!** W razie błędu przy uruchomieniu aplikacji `streamlit_dashboard.py` przy plikach pkl należy z folderu 
`src/ModelTraining` usunąć oba pliki `.pkl` (`label_encoders.pkl`, `random_forest_model.pkl`). Pliki tworzone były przy
użyciu pandas or numpy w wersji na macOS z ARM, w związku z czym może wystąpić drobny problem. Zostało to przetestowane 
na innym komputerze z macOS oraz Intelem. Po usunięciu plików należy uruchomić `train_random_forest.py`, aby uzyskać
pliki modelu, niezbędne dla dashboarda. Trening zajmuje dosłownie sekundę. Model oraz metryki mogą różnić się nieznacznie,
co jednak nie wpłynie na resztę projektu.

## Uwagi dodatkowe:
1. Projekt był formatowany przy użyciu biblioteki black.
2. Metody, których nazwy opisują jednoznacznie ich działanie, nie posiadają komentarzy.
3. Metody wymagający dopowiedzenia zawierają doc-stringi.
4. W projekcie istnieją dwa konta, wsiemiatkowski oraz s20404. s20404 to mój number indeksu i do tego konta token posiadam
w terminalu. Projekt założyłem na GitHubie z konta prywatnego.