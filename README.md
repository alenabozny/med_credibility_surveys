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
  * [x] dodać instrukcję
  * [x] dodać tagi
* Poprawki
    * [x] - przyciski back/save na dole  
    * [x] - przypisywanie tylko pustych taskow z danego artykułu
    * [x] - wybieranie, ktore zdania (co drugie, co trzecie) - w trakcie, ale nie wiem jak zapisac, czy dodanie kazdego zdania oddzielnie spowoduje n unikalnych taskow? --> wybieramy co 2/3 zdanie, sprawdzamy po kolei, czy dane zdanie ma już task przypisany do użytkownika innego niż aktywny. Zdania z Taskami przypisanymi innym użytkownikom zostawiamy w spokoju. Zdania bez Tasków - tworzymy Task i przypisujemy go aktywnemu użytkownikowi. 1 zdanie = 1 task
    * [x] - kolejne taski losowe, nie kolejne
    * [x] - imie/nazwisko usera
    * [x] - usunac usuwanie usera
    * [x] - wyswietlanie tresci zdania w admince
    * [x] - wyswietlanie tytulu artykulu w admince (przy taskach)
    * [x] - rózne wersje modyfikacji zdań (kopia artykułu)
    * [x] - w widoku użytkownika: możliwość zaznaczenia więcej niż jednego tasku i "odprzypisania" ich za jednym razem
    * [x] - addTask: wyświetlenie tylko tych zdań, które mają swój task
    * [x] - addTask: dla zaznaczonych checkboxem zdań przypisać taski z nimi powiązane edytowanemu użytkownikowi
    * [x] - wczytywanie daty (funkcja) - ISO,  yyyy-mm-dd,  dd-mm-yyyy
    * [x] - REMOVE SELECTED TASKS nie powinno czyścić ocenę; zmienić nazwę na UNASSIGN SELECTED TASKS
    * [x] - steps powinno rozpoczynać się od 0, a nie od 1
    * [x] - kolumna tags w Tasku powinna przyjmować do 500 znaków (na prod ustawiono ręcznie)

REVIEW
 * [ ] tabela Review + powiązania z użytkownikiem i taskiem
 * [ ] rola użytkownika is_reviewer
 * [ ] widok dodawania nowego Review
 * [ ] dodać 'category' do Article
