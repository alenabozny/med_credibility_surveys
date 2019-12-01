# med_credibility_surveys

## Dane do logowania

login: test
haslo: test

## TODO:
* skrypt ładujący artykuł:
  * [x] dzielenie artykułu na zdania
  * [x] dodawanie artykuły do bazy
  * [x] dodawanie zdań i powiązanych z nimi Tasków (Triggerem) do bazy
  * [ ] obliczanie i dodawanie słów kluczowych
* Widok edycji Tasku
-- BACKEND:
  * [x] Zapewnienie, że raz edytowany, nie będzie mógł być edytowany po raz kolejny
  * [x] Ograniczenie dostępu do tasków tylko powiązanym użytkownikom
  * [x] Aktualizacja tasku na podstawie forumlarza przekazywanego pod koniec edycji
  * [x] funkcja uzyskiwania prawego i lewego kontekstu z indeksami "bliskości"
* Widok edycji Tasku -- FRONTEND:
  * [x] Endpoint zwracający dane
  * [x] zliczanie czasu edycji tasku
  * [x] wysyłka formularza z wynikami oceny i wszystkimi metrykami (w tym tagi)
  * [x] poprawny odczyt prawego i lewego kontekstu
  * [x] wyświetlanie tagów po wyborze "noncredible"
* [x] Lista tasków na stronie użytkownika
  * [x] Endpoint zwracający dane
  * [x] Widok
* ADMINKA
  * [x] Przypisywanie tasków dotyczących zdań z wybranego artykułu do Usera
* KOSMETYKA
  * [ ] dodać instrukcję
  * [ ] dodać tagi
* Poprawki
    * [x] - przyciski back/save na dole  
    * [x] - przypisywanie tylko pustych taskow z danego artykułu
    * [ ] - wybieranie, ktore zdania (co drugie, co trzecie)
    * [x] - kolejne taski losowe, nie kolejne
    * [x] - imie/nazwisko usera
    * [x] - usunac usuwanie usera
    * [ ] - wczytywanie daty (funkcja) - ISO,  yyyy-mm-dd,  dd-mm-yyyy
    * [x] - wyswietlanie tresci zdania w admince
    * [x] - wyswietlanie tytulu artykulu w admince (przy taskach)
    * [ ] - rózne wersje modyfikacji zdań (kopia artykułu)
