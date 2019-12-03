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
    * [ ] - wybieranie, ktore zdania (co drugie, co trzecie) - w trakcie, ale nie wiem jak zapisac, czy dodanie kazdego zdania oddzielnie spowoduje n unikalnych taskow? --> wybieramy co 2/3 zdanie, sprawdzamy po kolei, czy dane zdanie ma już task przypisany do użytkownika innego niż aktywny. Zdania z Taskami przypisanymi innym użytkownikom zostawiamy w spokoju. Zdania bez Tasków - tworzymy Task i przypisujemy go aktywnemu użytkownikowi. 1 zdanie = 1 task
    * [x] - kolejne taski losowe, nie kolejne
    * [x] - imie/nazwisko usera
    * [x] - usunac usuwanie usera
    * [ ] - wczytywanie daty (funkcja) - ISO,  yyyy-mm-dd,  dd-mm-yyyy
    * [x] - wyswietlanie tresci zdania w admince
    * [x] - wyswietlanie tytulu artykulu w admince (przy taskach)
    * [x] - rózne wersje modyfikacji zdań (kopia artykułu)
    * [ ] - 3 stany checkboxu w widoku artykułu w admince:
     * 1. AKTYWNY NIEZAZNACZONY - Task do zdania jezcze nie istnieje. Zaznaczenie i zapisanie powoduje stworzenie Tasku dla zdania, który od razu zostanie przypisany edytowanemu użytkownikowi.
     * 2. AKTYWNY ZAZNACZONY - Task do zdania już istnieje i jest przypisany edytowanemu użytkownikowi. Odznaczenie i zapisanie zmian powoduje usunięcie Tasku.
     * 3. NIEAKTYWNY - Task do zdania już istnieje, ale jest przypisany innemu użytkownikowi.
    
