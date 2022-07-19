# See https://github.com/piccolo-orm/piccolo_admin/issues/173 for more info.

import typing as t

from pydantic import BaseModel, Field


###############################################################################
# Models
class TranslationListItem(BaseModel):
    language_name: str = Field(description="e.g. 'English'")
    language_code: str = Field(description="e.g. 'en'")


class TranslationListResponse(BaseModel):
    translations: t.List[TranslationListItem]
    default_language_code: str = Field(description="e.g. 'en'")


class Translation(BaseModel):
    """
    :param language_name:
        A human readable representation of the language. For example 'English'.
    :param language_code:
        The IETF language tag. For English it is 'en'. However, it also allows
        us to specify dialects like 'en-US' for American English, or 'en-GB'
        for British English, should we need it in the future.

    """

    language_name: str
    language_code: str
    translations: t.Dict[str, str]


###############################################################################
# Actual translations

# For now there aren't any words which are different between dialects, so we
# only need one form of English.
ENGLISH = Translation(
    language_name="English",
    language_code="en",
    translations={
        "About": "About",
        "Add Row": "Add Row",
        "Apply": "Apply",
        "Back": "Back",
        "Change password": "Change password",
        "Clear filters": "Clear filters",
        "Close": "Close",
        "Dark Mode": "Dark Mode",
        "Delete": "Delete",
        "Export CSV": "Export CSV",
        "Filter": "Filter",
        "Filters": "Filters",
        "Forms": "Forms",
        "Hide referencing tables": "Hide referencing tables",
        "Home": "Home",
        "Language": "Language",
        "Light Mode": "Light Mode",
        "Log out": "Log out",
        "Per page": "Per page",
        "Save": "Save",
        "Select one of the tables in the sidebar to get started.": (
            "Select one of the tables in the sidebar to get started."
        ),
        "Show filters": "Show filters",
        "Show referencing tables": "Show referencing tables",
        "Sort": "Sort",
        "Tables": "Tables",
        "Welcome to": "Welcome to",
    },
)

WELSH = Translation(
    language_name="Welsh",
    language_code="cy",
    translations={
        "About": "Am",
        "Add Row": "Ychwanegu Rhes",
        "Apply": "Ymgeisiwch",
        "Back": "Ol",
        "Change password": "Newid cyfrinair",
        "Clear filters": "Clirio hidlwyr",
        "Close": "Cau",
        "Dark Mode": "Modd Yywyll",
        "Delete": "Dileu",
        "Export CSV": "Allforio CSV",
        "Filter": "Ffilter",
        "Forms": "Ffurflenni",
        "Hide referencing tables": "Cuddio tablau cyfeirio",
        "Home": "Cartref",
        "Language": "Iaith",
        "Light Mode": "Modd Golau",
        "Log out": "Allgofnodi",
        "Per page": "Fesul tudalen",
        "Save": "Arbed",
        "Select one of the tables in the sidebar to get started.": (
            "Dewiswch un o'r tablau yn y bar ochr i ddechrau."
        ),
        "Show filters": "Dangos hidlwyr",
        "Show referencing tables": "Dangos tablau cyfeirio",
        "Sort": "Didoli",
        "Tables": "Tablau",
        "Welcome To": "Croeso i",
    },
)

CROATIAN = Translation(
    language_name="Croatian",
    language_code="hr",
    translations={
        "About": "O",
        "Add Row": "Dodaj redak",
        "Apply": "Primijeni",
        "Back": "Natrag",
        "Clear filters": "Obriši filtere",
        "Close": "Zatvori",
        "Dark Mode": "Tamni način rada",
        "Delete": "Izbriši",
        "Export CSV": "Izvezi CSV",
        "Filter": "Filtar",
        "Filters": "Filtere",
        "Hide": "Sakrij",
        "Home": "Početna",
        "Language": "Jezik",
        "Light Mode": "Svijetli način rada",
        "Log out": "Odjava",
        "Per page": "Po stranici",
        "Save": "Spremi",
        "Select one of the tables in the sidebar to get started.": (
            "Za početak odaberite jednu od tablica na bočnoj traci."
        ),
        "Welcome to": "Dobrodošli u",
        "Show filters": "Prikaži filtere",
        "Show": "Prikaži",
        "Create": "Kreiraj",
        "Sort": "Sortiraj",
        "Tables": "Tablice",
        "Change password": "Promijeni lozinku",
        "Weeks": "Tjedni",
        "Days": "Dani",
        "Hours": "Sati",
        "Minutes": "Minute",
        "Seconds": "Sekunde",
        "Form submitted": "Obrazac poslan",
        "Use again": "Koristi ponovno",
        "Back to home page": "Vrati se na početnu stranicu",
        "Go to page": "Idi na stranicu",
        "with a matching": "s odgovarajućom kolumnom",
        "Sort by": "Sortiraj po",
        "Forms": "Forme",
        "Current password": "Trenutna lozinka",
        "New password": "Nova lozinka",
        "New password confirmation": "Potvrda nove lozinke",
        "selected result(s) on": "odabranih rezultat(a) na",
        "page": "stranici",
        "Loading": "Učitavanje",
        "No results found": "Nema rezultata",
        "Showing": "Pokazuje",
        "of": "od",
        "result(s)": "rezultat(a)",
        "Version": "Verzija",
        "Thanks for using Piccolo Admin.": (
            "Hvala što koristite Piccolo Admin."
        ),
        "Edit": "Uredi",
        "Add": "Dodaj",
        "Ascending": "Uzlazno",
        "Descending": "Silazno",
        "rows": "redaka",
        "Select a column to update:": "Odaberite stupac za ažuriranje:",
        "Select a Column": "Odaberite stupac",
        "New value": "Nova vrijednost:",
        "Update": "Ažuriraj",
    },
)


TRANSLATIONS: t.List[Translation] = [ENGLISH, WELSH, CROATIAN]
