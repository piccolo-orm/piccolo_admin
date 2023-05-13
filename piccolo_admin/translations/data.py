"""
See https://github.com/piccolo-orm/piccolo_admin/issues/173 for more info.

NOTE: Flake8's line length warning has been disabled for this file - see
.flake8, so we don't have to worry about wrapping long translations.

NOTE: To validate the translations (to see if any are missing)::

    # At the root of the project
    python scripts/get_translations.py validate

NOTE: One of the fastest ways to get the translations in bulk is using Google
Spreadsheets. For example, this function translates a value from English to
Portuguese `=GOOGLETRANSLATE(A1,"en","pt")`. A CSV file can be downloaded, and
then converted to JSON using a tool like this
https://www.convertcsv.com/csv-to-json.htm.

"""

import typing as t

from piccolo_admin.translations.models import Translation

# For now there aren't any words which are different between dialects, so we
# only need one form of English.
ENGLISH = Translation(
    language_name="English",
    language_code="en",
    translations={
        "About": "About",
        "Add Row": "Add Row",
        "Add": "Add",
        "Apply": "Apply",
        "Ascending": "Ascending",
        "Back to home page": "Back to home page",
        "Back": "Back",
        "Change password": "Change password",
        "Charts": "Charts",
        "Clear filters": "Clear filters",
        "Close": "Close",
        "Create": "Create",
        "Current password": "Current password",
        "Dark Mode": "Dark Mode",
        "Days": "Days",
        "Delete": "Delete",
        "Descending": "Descending",
        "Edit": "Edit",
        "Export CSV": "Export CSV",
        "Filter": "Filter",
        "Form submitted": "Form submitted",
        "Forms": "Forms",
        "Go to page": "Go to page",
        "Hide Filters": "Hide Filters",
        "Hide referencing tables": "Hide referencing tables",
        "Home": "Home",
        "Hours": "Hours",
        "Light Mode": "Light Mode",
        "Loading": "Loading",
        "Log out": "Log out",
        "Login": "Login",
        "Minutes": "Minutes",
        "New password confirmation": "New password confirmation",
        "New password": "New password",
        "New value": "New value",
        "No results found": "No results found",
        "of": "of",
        "page": "page",
        "Password": "Password",
        "result(s)": "result(s)",
        "rows": "rows",
        "Save": "Save",
        "Seconds": "Seconds",
        "Select a column to update": "Select a column to update",
        "Select a Column": "Select a Column",
        "Select a table in the sidebar to get started.": "Select a table in the sidebar to get started.",
        "selected result(s) on": "selected result(s) on",
        "Show Filters": "Show filters",
        "Show referencing tables": "Show referencing tables",
        "Showing": "Showing",
        "Sort by": "Sort by",
        "Sort": "Sort",
        "Submit": "Submit",
        "Tables": "Tables",
        "Thanks for using Piccolo Admin.": "Thanks for using Piccolo Admin.",
        "Update": "Update",
        "Use again": "Use again",
        "Username": "Username",
        "Version": "Version",
        "Weeks": "Weeks",
        "Welcome to": "Welcome to",
        "with a matching": "with a matching",
    },
)


WELSH = Translation(
    language_name="Welsh",
    language_code="cy",
    translations={
        "About": "Am",
        "Add Row": "Ychwanegu Rhes",
        "Add": "Ychwanegu",
        "Apply": "Ymgeisiwch",
        "Ascending": "Esgynnol",
        "Back to home page": "Yn ôl i'r dudalen gartref",
        "Back": "Ol",
        "Change password": "Newid cyfrinair",
        "Charts": "Siartiau",
        "Clear filters": "Clirio hidlwyr",
        "Close": "Cau",
        "Create": "Creu",
        "Current password": "Cyfrinair cyfredol",
        "Dark Mode": "Modd Yywyll",
        "Days": "Dyddiau",
        "Delete": "Dileu",
        "Descending": "Disgyn",
        "Edit": "Golygu",
        "Export CSV": "Allforio CSV",
        "Filter": "Ffilter",
        "Form submitted": "Ffurflen wedi'i chyflwyno",
        "Forms": "Ffurflenni",
        "Go to page": "Ewch i'r dudalen",
        "Hide Filters": "Cuddio hidlwyr",
        "Hide referencing tables": "Cuddio tablau cyfeirio",
        "Home": "Cartref",
        "Hours": "Oriau",
        "Light Mode": "Modd Golau",
        "Loading": "Llwytho",
        "Log out": "Allgofnodi",
        "Login": "Mewngofnodi",
        "Minutes": "Munudau",
        "New password confirmation": "Cadarnhad cyfrinair newydd",
        "New password": "Cyfrinair newydd",
        "New value": "Gwerth newydd",
        "No results found": "Heb ganfod canlyniadau",
        "of": "o",
        "page": "tudalen",
        "Password": "Cyfrinair",
        "result(s)": "canlyniad(au)",
        "rows": "rhesi",
        "Save": "Arbed",
        "Seconds": "Eiliadau",
        "Select a column to update": "Dewiswch golofn i'w diweddaru",
        "Select a Column": "Dewiswch Golofn",
        "Select a table in the sidebar to get started.": "Dewiswch un o'r tablau yn y bar ochr i ddechrau.",
        "selected result(s) on": "canlyniad(au) dethol ymlaen",
        "Show Filters": "Dangos hidlwyr",
        "Show referencing tables": "Dangos tablau cyfeirio",
        "Showing": "Yn dangos",
        "Sort by": "Trefnu yn ôl",
        "Sort": "Didoli",
        "Submit": "Cyflwyno",
        "Tables": "Tablau",
        "Thanks for using Piccolo Admin.": "Diolch am ddefnyddio Piccolo Admin.",
        "Update": "Diweddariad",
        "Use again": "Defnyddiwch eto",
        "Username": "Enw defnyddiwr",
        "Version": "Fersiwn",
        "Weeks": "Wythnosau",
        "Welcome to": "Croeso i",
        "with a matching": "gyda chyfateb",
    },
)

CROATIAN = Translation(
    language_name="Croatian",
    language_code="hr",
    translations={
        "About": "O",
        "Add Row": "Dodaj redak",
        "Add": "Dodaj",
        "Apply": "Primijeni",
        "Ascending": "Uzlazno",
        "Back to home page": "Vrati se na početnu stranicu",
        "Back": "Natrag",
        "Change password": "Promijeni lozinku",
        "Charts": "Grafikoni",
        "Clear filters": "Obriši filtere",
        "Close": "Zatvori",
        "Create": "Kreiraj",
        "Current password": "Trenutna lozinka",
        "Dark Mode": "Tamni način rada",
        "Days": "Dani",
        "Delete": "Izbriši",
        "Descending": "Silazno",
        "Edit": "Uredi",
        "Export CSV": "Izvezi CSV",
        "Filter": "Filtar",
        "Form submitted": "Obrazac poslan",
        "Forms": "Forme",
        "Go to page": "Idi na stranicu",
        "Hide Filters": "Sakrij filtre",
        "Hide referencing tables": "Sakrij referentne tablice",
        "Home": "Početna",
        "Hours": "Sati",
        "Light Mode": "Svijetli način rada",
        "Loading": "Učitavanje",
        "Log out": "Odjava",
        "Login": "Prijaviti se",
        "Minutes": "Minute",
        "New password confirmation": "Potvrda nove lozinke",
        "New password": "Nova lozinka",
        "New value": "Nova vrijednost:",
        "No results found": "Nema rezultata",
        "of": "od",
        "page": "stranici",
        "Password": "Zaporka",
        "result(s)": "rezultat(a)",
        "rows": "redaka",
        "Save": "Spremi",
        "Seconds": "Sekunde",
        "Select a column to update": "Odaberite stupac za ažuriranje",
        "Select a Column": "Odaberite stupac",
        "Select a table in the sidebar to get started.": "Za početak odaberite jednu od tablica na bočnoj traci.",
        "selected result(s) on": "odabranih rezultat(a) na",
        "Show Filters": "Prikaži filtere",
        "Show referencing tables": "Prikaži referentne tablice",
        "Showing": "Pokazuje",
        "Sort by": "Sortiraj po",
        "Sort": "Sortiraj",
        "Submit": "Podnijeti",
        "Tables": "Tablice",
        "Thanks for using Piccolo Admin.": "Hvala što koristite Piccolo Admin.",
        "Update": "Ažuriraj",
        "Use again": "Koristi ponovno",
        "Username": "Korisničko ime",
        "Version": "Verzija",
        "Weeks": "Tjedni",
        "Welcome to": "Dobrodošli u",
        "with a matching": "s odgovarajućom kolumnom",
    },
)


PORTUGUESE = Translation(
    language_name="Portuguese",
    language_code="pt",
    translations={
        "About": "Sobre",
        "Add Row": "Adicionar linha",
        "Add": "Adicionar",
        "Apply": "Aplicar",
        "Ascending": "Ascendente",
        "Back to home page": "Voltar à página inicial",
        "Back": "Voltar atrás",
        "Change password": "Mudar senha",
        "Charts": "Gráficos",
        "Clear filters": "Limpar Filtros",
        "Close": "Fechar",
        "Create": "Criar",
        "Current password": "Senha atual",
        "Dark Mode": "Modo escuro",
        "Days": "Dias",
        "Delete": "Eliminar",
        "Descending": "descendente",
        "Edit": "Editar",
        "Export CSV": "Exportar CSV",
        "Filter": "Filtro",
        "Form submitted": "Formulário enviado",
        "Forms": "Formulários",
        "Go to page": "Ir para página",
        "Hide Filters": "Ocultar filtros",
        "Hide referencing tables": "Ocultar tabelas de referência",
        "Home": "Página inicial",
        "Hours": "Horas",
        "Light Mode": "Modo claro",
        "Loading": "Carregando",
        "Log out": "Sair",
        "Login": "Conecte-se",
        "Minutes": "Minutos",
        "New password confirmation": "Nova confirmação de senha",
        "New password": "Nova Senha",
        "New value": "Novo valor",
        "No results found": "Nenhum resultado encontrado",
        "of": "do",
        "page": "página",
        "Password": "Senha",
        "result(s)": "resultado(s)",
        "rows": "linhas",
        "Save": "Guardar",
        "Seconds": "Segundos",
        "Select a column to update": "Selecione uma coluna para atualizar",
        "Select a Column": "Selecione uma coluna",
        "Select a table in the sidebar to get started.": "Selecione uma tabela na barra lateral para começar.",
        "selected result(s) on": "Resultados selecionados (s) em",
        "Show Filters": "Mostrar filtros",
        "Show referencing tables": "Mostrar tabelas de referência",
        "Showing": "Mostrando",
        "Sort by": "Ordenar por",
        "Sort": "Ordenar",
        "Submit": "Enviar",
        "Tables": "Tabelas",
        "Thanks for using Piccolo Admin.": "Obrigado por usar Piccolo Admin.",
        "Update": "Atualizar",
        "Use again": "Use novamente",
        "Username": "Nome de usuário",
        "Version": "Versão",
        "Weeks": "Semanas",
        "Welcome to": "Bem-vindo ao",
        "with a matching": "com uma correspondência",
    },
)


GERMAN = Translation(
    language_name="German",
    language_code="de",
    translations={
        "About": "Über",
        "Add Row": "Zeile hinzufügen",
        "Add": "Hinzufügen",
        "Apply": "Anwenden",
        "Ascending": "Aufsteigend",
        "Back to home page": "Zurück zur Startseite",
        "Back": "Zurück",
        "Change password": "Passwort ändern",
        "Charts": "Diagramme",
        "Clear filters": "Filter löschen",
        "Close": "Schließen",
        "Create": "Anlegen",
        "Current password": "Jetziges Passwort",
        "Dark Mode": "Dunkler Modus",
        "Days": "Tage",
        "Delete": "Löschen",
        "Descending": "Absteigend",
        "Edit": "Bearbeiten",
        "Export CSV": "Exportieren nach CSV",
        "Filter": "Filter",
        "Form submitted": "Formular eingereicht",
        "Forms": "Formulare",
        "Go to page": "Gehen Sie zur Seite",
        "Hide Filters": "Filter ausblenden",
        "Hide referencing tables": "Referenzierungstabellen ausblenden",
        "Home": "Startseite",
        "Hours": "Std",
        "Light Mode": "Heller Modus",
        "Loading": "Wird geladen",
        "Log out": "Ausloggen",
        "Login": "Anmeldung",
        "Minutes": "Minuten",
        "New password confirmation": "Neues Passwort bestätigen",
        "New password": "Neues Passwort",
        "New value": "Neuer Wert",
        "No results found": "keine Ergebnisse gefunden",
        "of": "von",
        "page": "Seite",
        "Password": "Passwort",
        "result(s)": "Ergebnis(se)",
        "rows": "Zeilen",
        "Save": "Speichern",
        "Seconds": "Sekunden",
        "Select a column to update": "Wählen Sie eine Spalte aus, um zu aktualisieren",
        "Select a Column": "Wählen Sie eine Spalte aus",
        "Select a table in the sidebar to get started.": "Wählen Sie eine Tabelle in der Seitenleiste aus, um loszulegen.",
        "selected result(s) on": "ausgewählte(s) Ergebnis(se) auf",
        "Show Filters": "Filter anzeigen",
        "Show referencing tables": "Referenzierungstabellen anzeigen",
        "Showing": "Zeigen",
        "Sort by": "Sortieren nach",
        "Sort": "Sortieren",
        "Submit": "Abschicken",
        "Tables": "Tabellen",
        "Thanks for using Piccolo Admin.": "Vielen Dank für die Verwendung von Piccolo Admin.",
        "Update": "Aktualisieren",
        "Use again": "Wiederbenutzen",
        "Username": "Nutzername",
        "Version": "Version",
        "Weeks": "Wochen",
        "Welcome to": "Willkommen zu",
        "with a matching": "mit einem Matching",
    },
)


FRENCH = Translation(
    language_name="French",
    language_code="fr",
    translations={
        "About": "À propos de",
        "Add Row": "Ajouter une ligne",
        "Add": "Ajouter",
        "Apply": "Appliquer",
        "Ascending": "Croissant",
        "Back to home page": "Retour à la page d'accueil",
        "Back": "Retour",
        "Change password": "Changer le mot de passe",
        "Charts": "Graphiques",
        "Clear filters": "Supprimer les filtres",
        "Close": "Fermer",
        "Create": "Créer",
        "Current password": "Mot de passe actuel",
        "Dark Mode": "Mode sombre",
        "Days": "Journées",
        "Delete": "Effacer",
        "Descending": "Décroissant",
        "Edit": "Éditer",
        "Export CSV": "Exporter CSV",
        "Filter": "Filtre",
        "Form submitted": "Formulaire soumis",
        "Forms": "Formulaires",
        "Go to page": "Aller à la page",
        "Hide Filters": "Masquer les filtres",
        "Hide referencing tables": "Masquer les tables de référence",
        "Home": "Accueil",
        "Hours": "Heures",
        "Light Mode": "Mode léger",
        "Loading": "Chargement",
        "Log out": "Se déconnecter",
        "Login": "Connexion",
        "Minutes": "Minutes",
        "New password confirmation": "Confirmation du nouveau mot de passe",
        "New password": "Nouveau mot de passe",
        "New value": "Nouvelle valeur",
        "No results found": "Aucun résultat trouvé",
        "of": "de",
        "page": "page",
        "Password": "Mot de passe",
        "result(s)": "résultat(s)",
        "rows": "lignes",
        "Save": "Sauvegarder",
        "Seconds": "Secondes",
        "Select a column to update": "Sélectionnez une colonne à mettre à jour",
        "Select a Column": "Sélectionnez une colonne",
        "Select a table in the sidebar to get started.": "Sélectionnez une table dans la barre latérale pour commencer.",
        "selected result(s) on": "Résultats sélectionnés sur",
        "Show Filters": "Montrer les filtres",
        "Show referencing tables": "Afficher les tables de référence",
        "Showing": "Projection",
        "Sort by": "Trier par",
        "Sort": "Trier",
        "Submit": "Soumettre",
        "Tables": "les tables",
        "Thanks for using Piccolo Admin.": "Merci d'utiliser PicColo Admin.",
        "Update": "Mise à jour",
        "Use again": "Utiliser à nouveau",
        "Username": "Nom d'utilisateur",
        "Version": "Version",
        "Weeks": "Semaines",
        "Welcome to": "Bienvenue à",
        "with a matching": "avec une correspondance",
    },
)


SPANISH = Translation(
    language_name="Spanish",
    language_code="es",
    translations={
        "About": "Sobre",
        "Add Row": "Añadir fila",
        "Add": "Añadir",
        "Apply": "Aplicar",
        "Ascending": "Ascendente",
        "Back to home page": "Volver a la página de inicio",
        "Back": "atrás",
        "Change password": "Cambia la contraseña",
        "Charts": "Gráficos",
        "Clear filters": "Eliminar filtros",
        "Close": "Cerca",
        "Create": "Crear",
        "Current password": "Contraseña actual",
        "Dark Mode": "Modo oscuro",
        "Days": "Días",
        "Delete": "Borrar",
        "Descending": "Descendente",
        "Edit": "Editar",
        "Export CSV": "CSV de exportación",
        "Filter": "Filtrar",
        "Form submitted": "Formulario enviado",
        "Forms": "Formularios",
        "Go to page": "Ir a la página",
        "Hide Filters": "Ocultar filtros",
        "Hide referencing tables": "Ocultar tablas de referencia",
        "Home": "Hogar",
        "Hours": "Horas",
        "Light Mode": "Modo de luz",
        "Loading": "Cargando",
        "Log out": "Cerrar sesión",
        "Login": "Acceso",
        "Minutes": "Minutos",
        "New password confirmation": "Nueva confirmación de contraseña",
        "New password": "Nueva contraseña",
        "New value": "Nuevo valor",
        "No results found": "No se han encontrado resultados",
        "of": "de",
        "page": "página",
        "Password": "Clave",
        "result(s)": "resultado(s)",
        "rows": "hilera",
        "Save": "Ahorrar",
        "Seconds": "Segundos",
        "Select a column to update": "Seleccione una columna para actualizar",
        "Select a Column": "Seleccione una columna",
        "Select a table in the sidebar to get started.": "Seleccione una tabla en la barra lateral para comenzar.",
        "selected result(s) on": "Resultados seleccionados en",
        "Show Filters": "Mostrar filtros",
        "Show referencing tables": "Mostrar tablas de referencia",
        "Showing": "Demostración",
        "Sort by": "Ordenar por",
        "Sort": "Clasificar",
        "Submit": "Enviar",
        "Tables": "Tablas",
        "Thanks for using Piccolo Admin.": "Gracias por usar Piccolo Admin.",
        "Update": "Actualizar",
        "Use again": "Usar de nuevo",
        "Username": "Nombre de usuario",
        "Version": "Versión",
        "Weeks": "Semanas",
        "Welcome to": "Bienvenido a",
        "with a matching": "con un juego",
    },
)

FINNISH = Translation(
    language_name="Finnish",
    language_code="fi",
    translations={
        "About": "Tietoa",
        "Add Row": "Lisää rivi",
        "Add": "Lisää",
        "Apply": "Aseta",
        "Ascending": "Nouseva",
        "Back to home page": "Takaisin pääsivulle",
        "Back": "Takaisin",
        "Change password": "Vaihda salasana",
        "Charts": "Kaaviot",
        "Clear filters": "Nollaa suodattimet",
        "Close": "Sulje",
        "Create": "Luo",
        "Current password": "Nykyinen salasana",
        "Dark Mode": "Tumma tila",
        "Days": "Päivät",
        "Delete": "Poista",
        "Descending": "Laskeva",
        "Edit": "Muokkaa",
        "Export CSV": "Vie CSV",
        "Filter": "Suodata",
        "Form submitted": "Lomake lähetetty",
        "Forms": "Lomakkeet",
        "Go to page": "Mene sivulle",
        "Hide Filters": "Piilota suodattimet",
        "Hide referencing tables": "Piilota viitetaulukot",
        "Home": "Koti",
        "Hours": "Tunnit",
        "Light Mode": "Vaalea tila",
        "Loading": "Latautuu",
        "Log out": "Kirjaudu ulos",
        "Login": "Kirjaudu",
        "Minutes": "Minuutit",
        "New password confirmation": "Uusi salasana hyväksyntä",
        "New password": "Uusi salasana",
        "New value": "Uusi arvo",
        "No results found": "Ei löytynyt tuloksia",
        "of": "osa",
        "page": "sivu",
        "Password": "Salasana",
        "result(s)": "tulokset",
        "rows": "rivit",
        "Save": "Tallenna",
        "Seconds": "Sekunnit",
        "Select a column to update": "Valitse päivitettävä pystyrivi",
        "Select a Column": "Valitse pystyrivi",
        "Select a table in the sidebar to get started.": "Valitse taulu sivupalkista aloittaaksesi.",
        "selected result(s) on": "valitut tulokset",
        "Show Filters": "Näytä suodattimet",
        "Show referencing tables": "Näytä viitetaulut",
        "Showing": "Näkyvissä",
        "Sort by": "Lajittele jnkn mukaan",
        "Sort": "Lajittele",
        "Submit": "Lähetä",
        "Tables": "Taulukot",
        "Thanks for using Piccolo Admin.": "Kiitos, että käytät Piccolo Adminia.",
        "Update": "Päivitä",
        "Use again": "Käytä uudelleen",
        "Username": "Käyttäjänimi",
        "Version": "Versio",
        "Weeks": "Viikot",
        "Welcome to": "Tervetuloa",
        "with a matching": "osumalla",
    },
)

RUSSIAN = Translation(
    language_name="Russian",
    language_code="ru",
    translations={
        "About": "О продукте",
        "Add Row": "Добавить строку",
        "Add": "Добавить",
        "Apply": "Подтвердить",
        "Ascending": "По возрастанию",
        "Back to home page": "Вернуться на главную страницу",
        "Back": "Назад",
        "Change password": "Сменить пароль",
        "Charts": "Графики",
        "Clear filters": "Сбросить фильтры",
        "Close": "Закрыть",
        "Create": "Создать",
        "Current password": "Текущий пароль",
        "Dark Mode": "Темная тема",
        "Days": "Дни",
        "Delete": "Удалить",
        "Descending": "По убыванию",
        "Edit": "Изменить",
        "Export CSV": "Экспорт в CSV",
        "Filter": "Фильтр",
        "Form submitted": "Форма отправлена",
        "Forms": "Формы",
        "Go to page": "Перейти к странице",
        "Hide Filters": "Скрыть фильтры",
        "Hide referencing tables": "Скрыть связаные таблицы",
        "Home": "Главная",
        "Hours": "Часы",
        "Light Mode": "Светлая тема",
        "Loading": "Загрузка",
        "Log out": "Выйти",
        "Login": "Войти",
        "Minutes": "Минуты",
        "New password confirmation": "Повторите новый пароль",
        "New password": "Новый пароль",
        "New value": "Новое значение",
        "No results found": "Ничего не найдено",
        "of": "из",
        "page": "страницу(е)",
        "Password": "Пароль",
        "result(s)": "строк(и)",
        "rows": "строки",
        "Save": "Сохранить",
        "Seconds": "Секунды",
        "Select a column to update": "Выберите столбец для обновления",
        "Select a Column": "Выберите столбец",
        "Select a table in the sidebar to get started.": "Выберите таблицу в боковой панели.",
        "selected result(s) on": "выбрано на",
        "Show Filters": "Показать фильтры",
        "Show referencing tables": "Показать связанные таблицы",
        "Showing": "Показано",
        "Sort by": "Сортировать по",
        "Sort": "Сортировка",
        "Submit": "Отправить",
        "Tables": "Таблицы",
        "Thanks for using Piccolo Admin.": "Спасибо, что используете Piccolo Admin.",
        "Update": "Обновить",
        "Use again": "Использовать снова",
        "Username": "Логин",
        "Version": "Версия",
        "Weeks": "Недели",
        "Welcome to": "Добро пожаловать в",
        "with a matching": "c соответствующим",
    },
)

UKRAINIAN = Translation(
    language_name="Ukrainian",
    language_code="uk",
    translations={
        "About": "Про продукт",
        "Add Row": "Додати рядок",
        "Add": "Додати",
        "Apply": "Застосувати",
        "Ascending": "За зростанням",
        "Back to home page": "Повернутися на головну сторінку",
        "Back": "Назад",
        "Change password": "Змінити пароль",
        "Charts": "Діаграми",
        "Clear filters": "Очистити фільтри",
        "Close": "Закрити",
        "Create": "Створити",
        "Current password": "Поточний пароль",
        "Dark Mode": "Темна тема",
        "Days": "Дні",
        "Delete": "Видалити",
        "Descending": "За спаданням",
        "Edit": "Редагувати",
        "Export CSV": "Експорт в CSV",
        "Filter": "Фільтр",
        "Form submitted": "Форму відправлено",
        "Forms": "Форми",
        "Go to page": "Перейти на сторінку",
        "Hide Filters": "Приховати фільтри",
        "Hide referencing tables": "Приховати пов'язані таблиці",
        "Home": "Головна",
        "Hours": "Години",
        "Light Mode": "Світла тема",
        "Loading": "Завантаження",
        "Log out": "Вийти",
        "Login": "Увійти",
        "Minutes": "Хвилини",
        "New password confirmation": "Підтвердіть новий пароль",
        "New password": "Новий пароль",
        "New value": "Нове значення",
        "No results found": "Нічого не знайдено",
        "of": "з",
        "page": "сторінки",
        "Password": "Пароль",
        "result(s)": "результат(ів)",
        "rows": "рядки",
        "Save": "Зберегти",
        "Seconds": "Секунди",
        "Select a column to update": "Виберіть стовпчик для оновлення",
        "Select a Column": "Виберіть стовпчик",
        "Select a table in the sidebar to get started.": "Виберіть таблицю в бічній панелі.",
        "selected result(s) on": "вибрано на",
        "Show Filters": "Показати фільтри",
        "Show referencing tables": "Показати пов'язані таблиці",
        "Showing": "Показано",
        "Sort by": "Сортувати за",
        "Sort": "Сортування",
        "Submit": "Відправити",
        "Tables": "Таблиці",
        "Thanks for using Piccolo Admin.": "Дякуємо, що використовуєте Piccolo Admin. Рускій корабль іде нах@й!",
        "Update": "Оновити",
        "Use again": "Використати ще раз",
        "Username": "Ім'я користувача",
        "Version": "Версія",
        "Weeks": "Тижні",
        "Welcome to": "Ласкаво просимо до",
        "with a matching": "з пов'язаним",
    },
)

SIMPLIFIED_CHINESE = Translation(
    language_name="Simplified Chinese",
    language_code="zh-CN",
    translations={
        "About": "关于",
        "Add Row": "添加行",
        "Add": "添加",
        "Apply": "应用",
        "Ascending": "正序",
        "Back to home page": "返回主页",
        "Back": "返回",
        "Change password": "修改密码",
        "Charts": "图表",
        "Clear filters": "清除过滤器",
        "Close": "关闭",
        "Create": "创建",
        "Current password": "当前密码",
        "Dark Mode": "夜间模式",
        "Days": "天",
        "Delete": "删除",
        "Descending": "倒序",
        "Edit": "编辑",
        "Export CSV": "导出 CSV",
        "Filter": "过滤器",
        "Form submitted": "已提交的表单",
        "Forms": "表单",
        "Go to page": "转到页面",
        "Hide Filters": "隐藏过滤器",
        "Hide referencing tables": "隐藏引用的表",
        "Home": "主页",
        "Hours": "小时",
        "Light Mode": "白天模式",
        "Loading": "加载中",
        "Log out": "登出",
        "Login": "登录",
        "Minutes": "分钟",
        "New password confirmation": "确认新密码",
        "New password": "新密码",
        "New value": "新的值",
        "No results found": "没有找到结果",
        "of": "于",  # prep. is hard to translate in Chinese
        "page": "页",
        "Password": "密码",
        "result(s)": "结果",
        "rows": "行",
        "Save": "保存",
        "Seconds": "秒",
        "Select a column to update": "选择要更新的列",
        "Select a Column": "选择一个列",
        "Select a table in the sidebar to get started.": "请在侧栏选择一个表来开始编辑",
        "selected result(s) on": "选择的结果",
        "Show Filters": "显示过滤器",
        "Show referencing tables": "显示引用的表",
        "Showing": "正在显示",
        "Sort by": "使用排序",  # it should be 使用...排序
        "Sort": "排序",
        "Submit": "提交",
        "Tables": "表",
        "Thanks for using Piccolo Admin.": "感谢您使用 Piccolo 管理界面",
        "Update": "更新",
        "Use again": "再次使用",
        "Username": "用户名",
        "Version": "版本",
        "Weeks": "周",
        "Welcome to": "欢迎来到",
        "with a matching": "匹配了",  # it should be 与...匹配
    },
)


TURKISH = Translation(
    language_name="Turkish",
    language_code="tr",
    translations={
        "About": "Hakkında",
        "Add Row": "Kayıt Ekle",
        "Add": "Ekle",
        "Apply": "Uygula",
        "Ascending": "Artan sırada",
        "Back to home page": "Anasayfaya geri dön",
        "Back": "Geri dön",
        "Change password": "Şifreyi değiştir",
        "Charts": "Grafikler",
        "Clear filters": "Filtreleri temizle",
        "Close": "Kapat",
        "Create": "Oluştur",
        "Current password": "Mevcut şifre",
        "Dark Mode": "Gece Modu",
        "Days": "Günler",
        "Delete": "Sil",
        "Descending": "Azalan sırada",
        "Edit": "Güncelle",
        "Export CSV": "CSV Olarak Dışa Aktar",
        "Filter": "Filtre",
        "Form submitted": "Form gönderildi",
        "Forms": "Formlar",
        "Go to page": "Sayfaya git",
        "Hide Filters": "Filtreleri Gizle",
        "Hide referencing tables": "Referans tablolarını gizle",
        "Home": "Ana Sayfa",
        "Hours": "Saatler",
        "Light Mode": "Gündüz Modu",
        "Loading": "Yükleniyor",
        "Log out": "Çıkış yap",
        "Login": "Giriş",
        "Minutes": "Dakikalar",
        "New password confirmation": "Yeni şifre tekrarı",
        "New password": "Yeni şifre",
        "New value": "Yeni değer",
        "No results found": "Sonuç bulunamadı",
        "of": "of",
        "page": "sayfa",
        "Password": "Şifre",
        "result(s)": "kayıt(lar)",
        "rows": "satır",
        "Save": "Kaydet",
        "Seconds": "Saniyeler",
        "Select a column to update": "Güncelleme için bir sütun seç",
        "Select a Column": "Bir sütun seç",
        "Select a table in the sidebar to get started.": "Başlamak için kenar çubuğundaki bir tabloyu seçin.",
        "selected result(s) on": "seçilen kayıt(lar)",
        "Show Filters": "Filtreleri Göster",
        "Show referencing tables": "Referans tablolarını göster",
        "Showing": "Gösterilen",
        "Sort by": "Sırala",
        "Sort": "Sırala",
        "Submit": "Gönder",
        "Tables": "Tablolar",
        "Thanks for using Piccolo Admin.": "Piccolo Admin kullanımınız için teşekkür ederiz.",
        "Update": "Güncelle",
        "Use again": "Tekrar kullan",
        "Username": "Kullanıcı adı",
        "Version": "Versiyon",
        "Weeks": "Haftalar",
        "Welcome to": "Hoşgeldiniz",
        "with a matching": "ile eşleşen",
    },
)

TRANSLATIONS: t.List[Translation] = [
    ENGLISH,
    CROATIAN,
    FINNISH,
    FRENCH,
    GERMAN,
    PORTUGUESE,
    SIMPLIFIED_CHINESE,
    SPANISH,
    RUSSIAN,
    TURKISH,
    UKRAINIAN,
    WELSH,
]
