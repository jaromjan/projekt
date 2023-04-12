## Projekt końcowy
#### GRUPA 2. Przetwarzanie danych
#### Temat: 
- Porównanie zarobków na różnych stanowiskach branży it w różnych miastach w Indiach (Flask/CLI).
#### Opis:
#### Aplikacja używa bazy danych z tabeli:
#### https://www.kaggle.com/iamsouravbanerjee/analytics-industry-salaries-2022-india
#### Użytkownik wybiera miasto - Bangalore, Pune, Hyderabad, New Delhi, Mumbai
#### Aplikacja zwraca:
- Średnie roczne zarobki na każdym z dostępnych stanowisk w wybranym mieście
- 3 Firmy które płacą najwięcej w danym mieście, o ile procent powyżej
    średniej wynoszą zarobki w tych firmach  w porównaniu do średnich
    zarobków na danym stanowisku
- Rekomendacja jakie stanowisko w której firmie jest najbardziej opłacalne 
#### Opis rozwiązania:
- wybrano rozwiązanie oparte o bazę danych(sqlite), serwer FLASK i przeglądarkę
- wszystkie obliczenia wykonano za pomocą SQL
- przy pierwszym uruchomieniu w nowym środowisku tworzona jest baza danych na podstawie zawartości pliku csv
- załączony plik csv został pobrany ze wskazanej strony i wstępnie oczyszczony
#### Opis działania:
- po otwarciu strony w przeglądarce użytkownik ma do dyspozycji listę rozwijalną z nazwami miast, 
trzy przyciski: Analizuj dane, Wyczyść dane, Koniec oraz dwa linki do danych źródłowych i wikipedii
  (opis waluty w Indiach)
- po wybraniu miasta należy nacisnąć przycisk Analizuj dane, w kolejnych tabelach
zostaną wyświetlone wyniki, wybrane miasto jest nadal prezentowane jako wybrane w liście
- przycisk Wyczyść dane powoduje wyczyszczenie wyników i wybranej pozycji w liście miast
- przycisk Koniec przerywa połączenie z serwerem(konieczne jest ponowne otwarcie strony) 
