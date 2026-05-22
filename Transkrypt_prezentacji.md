# Transkrypt prezentacji — Software Quality Management

**Czas łączny: ~20 minut** • **Liczba słów: ~2 800** • **Tempo: ~140 słów/min**

Podział między autorów jest sugerowany — można go modyfikować. Każdy slajd ma osobny segment, oznaczony numerem slajdu i orientacyjnym czasem.

---

## 🎙️ CZĘŚĆ I — KONTEKST I PORÓWNANIE OGÓLNE *(prowadzi: Marcin)*

### 📑 Slajd 1 — Slajd tytułowy *(~30 sek)*

Dzień dobry. Tematem naszej prezentacji jest „Software Quality Management — studium porównawcze”. Wzięliśmy ten sam zestaw wymagań biznesowych: prosty CRUD użytkowników z autoryzacją, i zrealizowaliśmy go w dwóch wariantach. Pierwszy wariant — „quick and dirty”, zoptymalizowany pod szybkie dostarczenie. Drugi — „production-ready”, zoptymalizowany pod jakość, skalowalność i utrzymanie. W następnych dwudziestu minutach pokażemy państwu, jak bardzo te dwa światy różnią się od siebie. Prezentację przygotowali Marcin Skubisz, Miłosz Rataj i Artur Ścibor.

---

### 📑 Slajd 2 — Agenda *(~50 sek)*

Prezentację podzieliliśmy na sześć bloków. Najpierw pokażemy kontekst — dlaczego w ogóle warto porównywać dwa podejścia do tych samych wymagań. Następnie omówimy macierz jakości w dziewięciu wymiarach — od architektury, przez bezpieczeństwo, testy, aż po DevOps i dokumentację. Trzeci blok to antywzorce w wersji „simple” — czyli dług techniczny i jego konsekwencje przez cały cykl SDLC. Czwarty blok pokaże best practices w wersji „main” — Clean Code, Domain-Driven Design, Argon2id, Pydantic, Alembic, testy jednostkowe. Piąty blok to analiza kosztów i wartości — ile realnie kosztuje brak jakości, i co przynosi inwestycja w jakość. Na koniec pokażemy podsumowanie metryczne — konkretne liczby, które pokazują różnicę między tymi dwoma światami.

---

### 📑 Slajd 3 — Dwa podejścia *(~1 min)*

Zacznijmy od kontekstu. Oba projekty implementują dokładnie ten sam zakres funkcjonalny — CRUD użytkowników plus autoryzację. Identyczne endpointy, identyczne reguły biznesowe. Różni je tylko jedno: filozofia.

Po lewej stronie mamy backend_simple. Jest skupiony na czasie dostarczenia — Time-to-Market. Wszystko w jednym pliku, minimalna struktura. Brak walidacji, brak testów, brak migracji. Hasła trzymane w plaintekście, kontener uruchamiany jako root. Ten kod działa — dopóki nie spotka się z produkcją.

Po prawej — backend_main. Tu na pierwszym miejscu jest utrzymanie — Maintainability. Architektura warstwowa zgodnie z Domain-Driven Design. Pydantic, response_model, pełny Swagger. Trzynaście testów jednostkowych, SQLite in-memory. Argon2id z pepperem, non-root w Dockerze, migracje Alembic. Ten kod jest gotowy na zespół, na skalę i — co ważne — na refaktoryzację.

Ten sam business case. Dwa zupełnie różne światy jakości. I to właśnie chcemy pokazać.

---

### 📑 Slajd 4 — Macierz jakości *(~1 min 30 sek)*

Tutaj mamy macierz jakości w dziewięciu wymiarach.

Pierwszy wymiar — architektura. Po lewej monolit, gdzie wszystko leży w jednym pliku. Po prawej Domain-Driven Design z warstwami: api, core, database.

Walidacja danych. W simple — brak, albo ręczne if-else, które zawsze zapomnimy w którymś endpoincie. W main — Pydantic z silnym typowaniem; jeśli przyjdzie zły format, błąd wyłapie schemat, zanim w ogóle dotrzemy do bazy.

Obsługa błędów. Po lewej — każdy nieobsłużony wyjątek leci jako pięćset z pełnym stack trace. Po prawej — ustrukturyzowany ApiErrorResponse z modułem, typem błędu i semantycznym kodem HTTP.

Dokumentacja API. Bez response_model Swagger jest pusty. Z response_model i listą odpowiedzi w dekoratorze — Swagger staje się żywym kontraktem między backendem a frontendem.

Testy. Zero w simple — kod jest tak ciasno sprzężony, że nie da się go testować. Trzynaście testów w main, izolowanych w SQLite in-memory.

Zarządzanie bazą — hardcoded create_all kontra Alembic z pełną historią migracji.

Bezpieczeństwo — plaintext i root kontra Argon2id z pepperem i non-root user.

Observability — print w konsoli kontra strukturalne logowanie w formacie JSON.

I na koniec DevOps — single-stage Dockerfile kontra multi-stage build z healthchecks i dockerignore.

Dziewięć wymiarów — i w każdym jednym widać tę samą historię.

---

### 📑 Slajd 5 — backend_simple: antywzorce *(~1 min 30 sek)*

Przejdźmy teraz do konkretów po stronie negatywnej. Backend_simple to studium przypadku długu technicznego — przedstawimy sześć kluczowych antywzorców.

Pierwszy — brak separacji warstw. Logika HTTP, logika biznesowa i dostęp do bazy są wymieszane w jednym pliku main.py. Każda zmiana wymaga edycji tego samego pliku — co nieuchronnie prowadzi do konfliktów w gicie i regresji.

Drugi — plaintext hasła w bazie. Hasła zapisane są jak nazwiska. Co więcej, endpoint GET users/all zwraca je w czystej postaci. To nie tylko naruszenie najlepszych praktyk — to bezpośrednie naruszenie RODO, artykuł 32 mówiący o adekwatnych środkach technicznych.

Trzeci — brak testów uniemożliwia refaktoring. Tight coupling sprawia, że nie da się napisać testu jednostkowego — bo każda funkcja zna całą resztę aplikacji. W efekcie każda zmiana to ślepy strzał, a regresje wychodzą dopiero na produkcji.

Czwarty — niepowtarzalne buildy. Requirements.txt bez wersji plus pip install pobiera najnowsze pakiety. Dziś budujemy obraz z FastAPI 0.115, jutro z 0.116, pojutrze z 0.117 — i nagle coś przestaje działać. „Działa u mnie” staje się jedynym dowodem poprawności.

Piąty — globalna sesja bazy danych. SessionLocal tworzony globalnie, bez context managera. Brak rollbacka, wyciek pamięci, problemy ujawniają się dopiero pod realnym obciążeniem.

Szósty — root w Dockerze. Aplikacja uruchamiana jako root daje atakującemu, w razie container escape, pełne uprawnienia na hoście. CORS z allow_origins gwiazdka dopełnia obrazu — każda strona w internecie może wykonać request do naszego API.

To nie są błędy. To są świadome lub nieświadome skróty, które na końcu wystawiają fakturę zespołowi.

---

### 📑 Slajd 6 — backend_main: best practices *(~1 min 30 sek)*

A teraz strona pozytywna. Backend_main implementuje sześć fundamentalnych dobrych praktyk inżynierii oprogramowania.

Po pierwsze — architektura warstwowa. Warstwa api zawiera kontrolery FastAPI i schematy Pydantic. Warstwa core zawiera handlery z logiką biznesową oraz repozytoria do bazy. Warstwa database to modele SQLAlchemy, sesja i migracje. Każda warstwa zna tylko swoją odpowiedzialność — i tylko swoją.

Po drugie — bezpieczeństwo by design. Argon2id, czyli zwycięzca konkursu Password Hashing Competition z 2015 roku, plus pepper trzymany w zmiennej środowiskowej, czyli poza bazą. EmailStr i walidatory Pydantic na poziomie schematu. CORS zawężony do localhost na porcie 3000.

Po trzecie — testy jednostkowe z fixturami. Warstwa repozytorium pokryta jest trzynastoma testami w sześciu plikach. SQLite in-memory pozwala uruchamiać testy bez Postgresa — co znaczy, że CI nie musi podnosić bazy. Pytest plus conftest.py z fixturami engine, db_session i test_user.

Po czwarte — Alembic, czyli wersjonowane migracje. Każda zmiana schematu to jeden plik w katalogu versions. Rollback jedną komendą. Connection pool ze sztywno ustawionymi parametrami: pool_size 20, max_overflow 10, pre_ping włączone.

Po piąte — multi-stage Dockerfile. Non-root user, healthcheck, dockerignore. Docker Compose z warunkiem service_healthy, więc aplikacja startuje dopiero, gdy baza odpowiada. Osobne pliki środowiskowe: local.env i stg.env.

Po szóste — automatyzacja. Pyproject.toml plus uv, który jest od dziesięciu do stu razy szybszy od pip. Makefile z piętnastoma plus targetami. Deterministyczne buildy z uv.lock. CI/CD z bramkami jakości — lint, typy, testy, security scan.

---

## 🎙️ CZĘŚĆ II — GŁĘBOKIE PORÓWNANIE TECHNICZNE *(prowadzi: Miłosz)*

### 📑 Slajd 7 — Architektura *(~1 min)*

Przejdźmy teraz w głąb. Architektura to fundament — i tu różnica jest najbardziej widoczna.

Po lewej widzimy monolit. Jeden plik, main.py, w którym żyje wszystko: routing FastAPI, schematy Pydantic, logika biznesowa, zapytania SQLAlchemy, hashowanie haseł, sesja bazy, walidacja wejścia, obsługa błędów, logging. Wszystko sprzężone, wszystko zależy od wszystkiego. Tight coupling. Konsekwencja jest taka, że testy jednostkowe są niemożliwe, a każda zmiana ryzykuje regresją w nieoczekiwanym miejscu.

Po prawej — trzy wyraźne warstwy. Warstwa api zawiera tylko kontakt z HTTP: kontrolery, schematy, response_model. Warstwa core dzieli się na handlery z logiką biznesową oraz repozytoria do dostępu do bazy. Warstwa database to modele SQLAlchemy, sesja i migracje Alembic.

Co najważniejsze — warstwy komunikują się jasnym kontraktem: tuple data, error, ok. Repository zwraca trójkę, handler ją interpretuje, kontroler tłumaczy na HTTP. Dzięki temu każdą warstwę można testować w izolacji. Refaktoryzacja staje się bezpieczna. Nowy developer rozumie strukturę w piętnaście minut.

---

### 📑 Slajd 8 — Bezpieczeństwo *(~1 min 30 sek)*

Bezpieczeństwo to obszar, gdzie skróty kosztują najwięcej — bo płaci się za nie nie tylko czasem, ale również reputacją i pieniędzmi.

Pokażmy konkretny przykład: zapis hasła użytkownika do bazy.

Po lewej — w backend_simple — robimy INSERT INTO users z kolumną password ustawioną na surowy tekst hasła. „MojeHaslo123!” trafia do tabeli dokładnie tak, jak je użytkownik wpisał. Co to oznacza w praktyce? Każdy backup bazy, każde logi zapytań, każdy zrzut dla deweloperów — zawiera hasła w czystej postaci. Endpoint GET users/all zwraca je wszystkie. Brak walidatorów EmailStr — można się zarejestrować z dowolnym ciągiem znaków. CORS gwiazdka. Każdy endpoint publiczny. To bezpośrednie naruszenie RODO — artykuł trzydziesty drugi mówi o adekwatnych środkach technicznych dla danych osobowych. Kary mogą sięgać czterech procent rocznego obrotu firmy.

Po prawej — backend_main. Hasło przechodzi przez funkcję argon2.hash, do której dokładamy pepper trzymany w zmiennej środowiskowej. W bazie zapisujemy ciąg w formacie dolar argon2id dolar v równa się 19 — czyli hash zawierający też wersję algorytmu, parametry pamięci, czasu i równoległości oraz sól. Argon2id to algorytm, który wygrał konkurs Password Hashing Competition w 2015 roku — jest dziś standardem OWASP. Pepper trzymany w env oznacza, że nawet w razie wycieku samej bazy hasła pozostają bezpieczne. EmailStr i walidatory Pydantic odrzucają nieprawidłowe formaty na poziomie schematu. CORS jest zawężony do localhost. Pole password nigdy nie opuszcza serwera — żaden response_model go nie zawiera.

To różnica między „przepraszamy, mieliśmy incydent” a „mieliśmy incydent, ale dane są bezpieczne”.

---

### 📑 Slajd 9 — Obsługa błędów *(~1 min)*

Obsługa błędów to drugi obszar, gdzie widać dojrzałość kodu.

Wzorzec antypatyczny widzimy na górze. Endpoint pobiera użytkownika po id metodą one. Gdy id nie istnieje, SQLAlchemy rzuca wyjątek NoResultFound. Wyjątek leci w górę, FastAPI łapie go domyślnym handlerem, zwraca HTTP 500 i pełny stack trace. Z punktu widzenia klienta — pięćset to znaczy „serwer się popsuł”. A naprawdę chodziło tylko o to, że szukany rekord nie istnieje, co powinno być czterysta cztery, czyli Not Found.

Wzorzec dojrzały — błąd jako wartość. Repository zwraca trójkę: dane, błąd, flaga ok. Handler sprawdza flagę. Jeśli operacja się nie udała, woła error_response z modułem „user”, typem błędu „not_found” i kodem HTTP 404. Jeśli się udała — zwraca ApiSuccessResponse z danymi. Kontroler tłumaczy to na właściwy kod HTTP.

Korzyść jest podwójna. Po pierwsze, kody są semantyczne: 404 dla brakującego rekordu, 401 dla braku autoryzacji, 409 dla konfliktu — na przykład próby rejestracji z istniejącym emailem, 500 zarezerwowane wyłącznie dla rzeczywistej awarii serwera. Po drugie, struktura błędu jest stała — frontend wie, czego się spodziewać. Stack trace nigdy nie opuszcza serwera.

---

### 📑 Slajd 10 — Dokumentacja API *(~1 min)*

Swagger to żywy kontrakt między backendem a frontendem. Pytanie tylko, czy tego kontraktu naprawdę używamy.

Po lewej backend_simple. Endpoint GET users/all jest w Swaggerze widoczny, ale nie ma response_model. Swagger pokazuje tylko, że jest odpowiedź 200, bez schematu. Nie wiemy, czy to lista, czy obiekt, jakie pola, jakie typy. Brak summary, brak description, brak tagów. Kody błędów niewidoczne w specyfikacji. Kod obsługi błędów duplikuje się w każdym endpoincie. Frontend integruje się „na ślepo” — najpierw woła endpoint, potem patrzy w odpowiedzi, jakie pola są.

Po prawej — backend_main. Endpoint POST register ma response_model ustawiony na ApiSuccessResponse parametryzowany UserDTO. Ma listę responses z konkretnymi kodami błędów: 409 dla duplikatu emaila, 500 dla awarii. Ma summary, description i tag. Wspólna funkcja error_response zapobiega duplikacji. Co najważniejsze — frontend może wygenerować typy TypeScript bezpośrednio z OpenAPI. Kontrakt jest jeden, w jednym miejscu, automatycznie zsynchronizowany.

Pełny Swagger pod adresem /docs to nie luksus — to redukcja czasu integracji o połowę.

---

### 📑 Slajd 11 — Testy automatyczne *(~1 min 30 sek)*

Testy to obszar, w którym różnica jest najbardziej drastyczna.

Po lewej, w backend_simple — zero. Pokrycie zero procent. Każda refaktoryzacja to loteria. Każdy bugfix wymaga ręcznego testowania całej aplikacji. Po pewnym czasie zespół zaczyna unikać dotykania pewnych części kodu — bo „jakoś działają”. Kod zamarza. Dług techniczny rośnie wykładniczo.

Po prawej — trzynaście testów rozłożonych po sześciu plikach. Każda operacja repozytorium — login, register, one, collection, update, delete — ma dedykowany plik z dwoma–trzema testami: happy path i error path. Pokrycie warstwy repo sięga stu procent.

Po prawej widzimy strukturę. Plik conftest.py zawiera fixtures wspólne dla wszystkich testów: engine na poziomie sesji testowej, db_session na poziomie pojedynczej funkcji, oraz test_user — pomocniczy obiekt do testów wymagających istniejącego rekordu.

Trzy kluczowe decyzje. Po pierwsze, SQLite in-memory zamiast Postgresa. To znaczy, że CI nie potrzebuje uruchomionej bazy. Cały zestaw testów odpala się w sekundach, lokalnie i w pipeline'ie. Po drugie, fixtures pytest zapewniają izolację — każdy test dostaje świeży stan bazy. Po trzecie, jedna komenda make test uruchamia całość deterministycznie.

Refaktoryzacja przestaje być strachem. Staje się rutynową czynnością — bo testy złapią regresję, zanim dotrze ona do PRa.

---

### 📑 Slajd 12 — Baza danych *(~1 min)*

Baza danych to obszar, gdzie skróty kosztują najwięcej operacyjnie — bo każdy błąd schematu na produkcji to potencjalna utrata danych.

W backend_simple używamy konstrukcji Base.metadata.create_all. Przy starcie aplikacji SQLAlchemy ogląda modele i tworzy brakujące tabele. Brzmi wygodnie — i jest, dopóki nie potrzebujemy zmienić schematu. Bo create_all niczego nie modyfikuje — jeśli tabela istnieje, zostawia ją w spokoju. Każda zmiana wymaga ręcznego DROP TABLE na produkcji, z całą utratą danych. Rollback jest niemożliwy. Brak historii zmian — schemat „magicznie” pojawia się, gdy aplikacja wstaje. Globalna sesja prowadzi do wycieków pamięci. Brak connection poola.

W backend_main z Alembic dostajemy pełną kontrolę. Każda zmiana schematu to plik migracyjny w katalogu versions, z funkcjami upgrade i downgrade. Polecenie alembic upgrade head wykonuje migracje. Alembic downgrade -1 cofa ostatnią. Wersjonowanie i odwracalność. Sesja zarządzana jest przez managed_session, czyli context manager z automatycznym rollback przy wyjątku. Connection pool z parametrami pool_size, max_overflow i pre_ping zapewnia odporność na utratę połączeń. Audit trail przez Envers lub osobne tabele w schemacie audit. Liquibase performance data z kontekstami pozwala seedować dane różne dla różnych środowisk.

To różnica między „mam nadzieję, że migracja zadziała” a „migracja zadziała, a jeśli nie — wrócę do poprzedniego stanu jedną komendą”.

---

### 📑 Slajd 13 — Konteneryzacja *(~1 min)*

Konteneryzacja jest dziś standardem — ale Dockerfile można napisać dobrze albo źle.

Po lewej, klasyczny single-stage. FROM python 3.11, kopiujemy wszystko, instalujemy zależności, uruchamiamy uvicorn. Pięć linijek, działa. Ale: USER domyślnie root. Brak dockerignore — sekrety, katalog git, lokalne pliki, wszystko trafia do obrazu. Brak healthchecka — orkiestrator nie ma jak sprawdzić, czy aplikacja jest gotowa. Docker Compose nie czeka na bazę. Wszystkie środowiska używają tego samego pliku env.

Po prawej multi-stage build. Stage builder oparty na obrazie slim instaluje zależności poleceniem uv sync --frozen --no-dev. Stage runtime też slim, ale tylko z artefaktem aplikacji. Tworzymy użytkownika app i ustawiamy USER app, czyli non-root. Dodajemy HEALTHCHECK z curlem na endpoint health. Plik dockerignore wyklucza .git i sekrety. Docker Compose definiuje warunek service_healthy — aplikacja startuje dopiero, gdy baza jest gotowa do akceptowania połączeń. Osobne pliki env: local.env dla deweloperów, stg.env dla stagingu.

Obraz jest mniejszy, bezpieczniejszy, i orkiestrator wie, kiedy aplikacja naprawdę jest gotowa.

---

## 🎙️ CZĘŚĆ III — DEVOPS, KOSZT, WARTOŚĆ I PODSUMOWANIE *(prowadzi: Artur)*

### 📑 Slajd 14 — Zależności i CI/CD *(~1 min 15 sek)*

Połączyliśmy tu dwa tematy: zarządzanie zależnościami i pipeline CI/CD.

Po lewej, requirements.txt — fastapi, sqlalchemy, uvicorn, bez podanych wersji. To znaczy, że pip install pobierze zawsze najnowszą wersję. Każdy build może mieć inny zestaw bibliotek. „Działa u mnie” staje się jedynym dowodem.

Po prawej, pyproject.toml plus uv.lock. W pyproject deklarujemy semantyczne wersje. Uv generuje plik uv.lock z dokładnymi hashami każdego pakietu i zależności tranzytywnych. Komenda uv sync --frozen instaluje dokładnie te wersje. Uv jest do stu razy szybsze od pip. I co najważniejsze — build jest deterministyczny. Ten sam kod plus ten sam lock zawsze daje ten sam obraz.

Niżej CI/CD pipeline z sześcioma bramkami. Lint przez Ruff. Sprawdzenie typów przez Mypy. Skanowanie bezpieczeństwa przez Bandit. Testy jednostkowe z pytest i SQLite. Build obrazu multi-stage. Deploy z weryfikacją healthchecka. Każdy commit przechodzi przez ten pipeline, zanim trafi na main. Błędy wyłapywane są przed mergem, nie po deploymencie.

I na dole — esencja całego podejścia: onboarding nowego developera to dwie komendy. Make install, make run. Wszystko inne jest automatyzowane.

---

### 📑 Slajd 15 — Koszt długu technicznego *(~1 min 15 sek)*

Pora na rachunek. „Działa na moim komputerze” brzmi niewinnie — ale generuje sześć faktur, które przychodzą później.

Faktura pierwsza — plaintext hasła. Naruszenie danych to nie tylko katastrofa wizerunkowa. To realne kary finansowe z RODO sięgające czterech procent rocznego obrotu firmy. Dla firmy o obrotach stu milionów to cztery miliony jednorazowo.

Faktura druga — brak migracji. Każda zmiana schematu wymaga ręcznego DROP TABLE na produkcji. Każdy DROP TABLE to potencjalny downtime i ryzyko utraty danych klientów.

Faktura trzecia — globalna sesja bazy. Wyciek pamięci nie pojawia się w testach. Pojawia się w nocy, po deploymencie, gdy ruch produkcyjny zaczyna rosnąć. Wtedy ktoś musi wstać i to naprawić.

Faktura czwarta — brak testów. Refaktoryzacja staje się niemożliwa bez ryzyka regresji. Kod zamarza. Każdy boi się go dotknąć. Po roku zespół spowalnia o połowę.

Faktura piąta — brak response_model. Swagger jest bezużyteczny. Konsumenci API nie wiedzą, czego się spodziewać. Integracje wybuchają, zespoły frontendowe pracują wolniej, każda zmiana wymaga manualnej koordynacji.

Faktura szósta — root w Dockerze. Container escape to znana klasa podatności. Jeden CVE w libc, jeden exploit — i atakujący ma całą maszynę, a często całą sieć wewnętrzną.

Tych sześciu faktur nie widać w tygodniu pierwszym. Ale widać je w kwartale czwartym.

---

### 📑 Slajd 16 — Wartość inwestycji w jakość *(~1 min 15 sek)*

Po drugiej stronie — wartość inwestycji. Każda decyzja architektoniczna w backend_main procentuje przez cały cykl życia produktu.

Warstwowa architektura. Nowy developer rozumie strukturę w piętnaście minut, nie trzy godziny. Każda warstwa testowalna izolowanie. Onboarding staje się przewidywalny.

Alembic. Zmiana schematu to jeden plik migracji. Rollback jedną komendą. Pełna historia w git — możemy odtworzyć, kiedy i dlaczego dodano kolumnę.

Argon2id z pepperem. Bezpieczeństwo haseł zgodne ze standardami OWASP 2024. Fundament pod JWT, autoryzację ról, refresh tokens — wszystko to można zbudować na bazie tej decyzji.

Pydantic plus response_model. Błędy walidacji wykrywane przed dotarciem do bazy danych. Swagger generuje pełny kontrakt automatycznie. Frontend generuje typy z OpenAPI. Trzy korzyści w jednym narzędziu.

Testy jednostkowe. Refaktoryzacja bez strachu. Regresje wykrywane natychmiast, przez pipeline, przed mergem do main. CI nie wymaga PostgreSQL — testy działają wszędzie.

Makefile i CI/CD. Onboarding to dwie komendy. Bramki jakości wyłapują błędy automatycznie. Cały zespół pracuje na tych samych standardach, bo standardy są w kodzie, nie w głowach.

Te decyzje wymagają trochę więcej czasu na początku projektu. Ale ten czas oszczędza się wielokrotnie w każdym kolejnym miesiącu.

---

### 📑 Slajd 17 — Podsumowanie metryczne *(~1 min)*

Spójrzmy na liczby. Backend_simple ma około sześciu plików Pythona, jedną warstwę architektoniczną — czyli monolit. Backend_main — pięćdziesiąt plus plików w trzech warstwach: api, core, database.

Testy — zero w simple, trzynaście plików w main, pokrywających sześć operacji po dwa do trzech testów każda.

Pokrycie warstwy repo — zero procent kontra około stu procent z testami zarówno happy, jak i error path.

Dokumentacja endpointów — niekompletna kontra pełna, z response_model i kodami błędów.

Krytyczne podatności bezpieczeństwa — co najmniej pięć w simple, zero w main.

Czas onboardingu nowego developera — wysoki w simple, brak dokumentacji procesu. Niski w main: make install, make run.

Rollback schematu bazy — niemożliwy w simple, jedna komenda w main: alembic downgrade.

Deterministyczność buildu — nie w simple, tak w main dzięki uv.lock.

Wnioskując: jakość kosztuje na początku. Brak jakości kosztuje przez cały cykl życia produktu.

---

### 📑 Slajd 18 — Zakończenie *(~30 sek)*

Wniosek końcowy mieści się w jednym zdaniu. Jakość to inwestycja, a nie koszt. Każda dobra decyzja architektoniczna procentuje na każdym etapie SDLC — od onboardingu, przez development, testowanie, deployment, aż po utrzymanie. Każdy skrót — wraca w postaci faktury. Czasem małej, czasem ogromnej. Ale zawsze wraca.

Dziękujemy państwu za uwagę. Chętnie odpowiemy na pytania.

---

## 📊 PODZIAŁ CZASU

| Część | Slajdy | Czas | Prowadzi |
|:---|:---|:---:|:---|
| I. Kontekst i porównanie ogólne | 1–6 | ~6 min 50 sek | Marcin |
| II. Głębokie porównanie techniczne | 7–13 | ~8 min 30 sek | Miłosz |
| III. DevOps, koszt, wartość i podsumowanie | 14–18 | ~5 min 15 sek | Artur |
| **Łącznie** | **18** | **~20 min 35 sek** | **3 osoby** |

> Czasy są orientacyjne — przy spokojniejszym tempie prezentacja zmieści się w okolicach dwudziestu minut. Jeśli zostanie więcej czasu (zwykle zostaje), można poświęcić go na Q&A.

## 💡 WSKAZÓWKI PREZENTERSKIE

- **Płynne przejścia** — przy zmianie prowadzącego (po slajdzie 6 i po slajdzie 13) warto krótko przedstawić następną osobę: „Teraz Miłosz pokaże szczegóły techniczne” / „Artur podsumuje koszty i wartość”.
- **Slajdy z kodem** (8, 9, 12, 13, 14) — daj słuchaczom dwie–trzy sekundy na zobaczenie kodu, zanim zaczniesz mówić. Nie czytaj kodu na głos.
- **Tabele** (4, 17) — nie czytaj wszystkich wierszy. Wybierz najmocniejsze pozycje, resztę zostaw słuchaczom do samodzielnego przeczytania.
- **Slajd 18** — po zdaniu kończącym zrób krótką pauzę. Nie spiesz się z „dziękujemy”.
- **Q&A** — przygotujcie krótkie odpowiedzi na trzy najbardziej prawdopodobne pytania: „dlaczego nie po prostu zaczniemy od simple i przepiszemy później?”, „ile czasu zajmuje ten dodatkowy nakład pracy?”, „czy w małym projekcie też się to opłaca?”.
