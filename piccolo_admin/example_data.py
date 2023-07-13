import datetime
import typing as t
from decimal import Decimal

DIRECTORS: t.List[t.Dict[str, t.Any]] = [
    {
        "id": 1,
        "name": "Peter Jackson",
        "years_nominated": [2002, 2004],
        "gender": "m",
    },
    {
        "id": 2,
        "name": "George Lucas",
        "years_nominated": [1974, 1978],
        "gender": "m",
    },
    {"id": 3, "name": "J.J. Abrams", "years_nominated": [], "gender": "m"},
    {"id": 4, "name": "Gareth Edwards", "years_nominated": [], "gender": "m"},
    {"id": 5, "name": "Irvin Kershner", "years_nominated": [], "gender": "m"},
    {
        "id": 6,
        "name": "Richard Marquand",
        "years_nominated": [],
        "gender": "m",
    },
    {"id": 7, "name": "Rian Johnson", "years_nominated": [], "gender": "m"},
    {
        "id": 8,
        "name": "Ron Howard",
        "years_nominated": [2002, 2009],
        "gender": "m",
    },
]


MOVIES: t.List[t.Dict[str, t.Any]] = [
    {
        "name": "Star Wars: Episode IV - A New Hope",
        "rating": 93.3,
        "duration": datetime.timedelta(minutes=125),
        "director": 2,
        "description": (
            "After Princess Leia, the leader of the Rebel Alliance, is held "
            "hostage by Darth Vader, Luke and Han Solo must free her and "
            "destroy the powerful weapon created by the Galactic Empire."
        ),
        "release_date": datetime.date(year=1977, month=12, day=27),
        "oscar_nominations": 11,
        "won_oscar": True,
        "box_office": Decimal("775.5"),
        "barcode": 3999361649,
        "genre": 2,
    },
    {
        "name": "The Empire Strikes Back",
        "rating": 94.0,
        "duration": datetime.timedelta(minutes=127),
        "director": 5,
        "description": (
            "Darth Vader is adamant about turning Luke Skywalker to the dark "
            "side. Master Yoda trains Luke to become a Jedi Knight while his "
            "friends try to fend off the Imperial fleet."
        ),
        "release_date": datetime.date(year=1980, month=5, day=20),
        "oscar_nominations": 4,
        "won_oscar": True,
        "box_office": Decimal("547.9"),
        "barcode": 2384023507,
        "genre": 2,
    },
    {
        "name": "Return of the Jedi",
        "rating": 82.0,
        "duration": datetime.timedelta(minutes=136),
        "director": 6,
        "description": (
            "Luke Skywalker attempts to bring his father back to the light "
            "side of the 'Force'. At the same time, the rebels hatch a plan "
            "to destroy the second Death Star."
        ),
        "release_date": datetime.date(year=1983, month=6, day=2),
        "oscar_nominations": 5,
        "won_oscar": True,
        "box_office": Decimal("475.3"),
        "barcode": 9874111507,
        "genre": 2,
    },
    {
        "name": "Star Wars: Episode I – The Phantom Menace",
        "rating": 53.0,
        "duration": datetime.timedelta(minutes=136),
        "director": 2,
        "description": (
            "Two Jedi Knights set out to search for someone who can "
            "bring peace to the Force. Their search ends when they come "
            "across a young, gifted boy. But the Sith returns to stake claim "
            "to the Force."
        ),
        "release_date": datetime.date(year=1999, month=7, day=16),
        "oscar_nominations": 3,
        "won_oscar": False,
        "box_office": Decimal("1027.0"),
        "barcode": 4637581510,
        "genre": 2,
    },
    {
        "name": "Star Wars: Episode II – Attack of the Clones",
        "rating": 65,
        "duration": datetime.timedelta(minutes=144),
        "director": 2,
        "description": (
            "While pursuing an assassin, Obi Wan uncovers a sinister plot to "
            "destroy the Republic. With the fate of the galaxy hanging in the "
            "balance, the Jedi must defend the galaxy against the evil Sith."
        ),
        "release_date": datetime.date(year=2002, month=5, day=16),
        "oscar_nominations": 1,
        "won_oscar": False,
        "box_office": Decimal("653.0"),
        "barcode": 8392825607,
        "genre": 2,
    },
    {
        "name": "Star Wars: Episode III – Revenge of the Sith",
        "rating": 80.0,
        "duration": datetime.timedelta(minutes=140),
        "director": 2,
        "description": (
            "Anakin joins forces with Obi-Wan and sets Palpatine free from "
            "the evil clutches of Count Doku. But he falls prey to mind games "
            "that are played by Palpatine and the Jedis and gives into "
            "temptation."
        ),
        "release_date": datetime.date(year=2005, month=5, day=19),
        "oscar_nominations": 1,
        "won_oscar": False,
        "box_office": Decimal("868.4"),
        "barcode": 5174272602,
        "genre": 2,
    },
    {
        "name": "Star Wars: The Force Awakens",
        "rating": 93.0,
        "duration": datetime.timedelta(minutes=135),
        "director": 3,
        "description": (
            "A new order threatens to destroy the New Republic. Finn, Rey and "
            "Poe, backed by the Resistance and the Republic, must find a way "
            "to stop them and find Luke, the last surviving Jedi."
        ),
        "release_date": datetime.date(year=2015, month=12, day=17),
        "oscar_nominations": 5,
        "won_oscar": False,
        "box_office": Decimal("2068.0"),
        "barcode": 9476361634,
        "genre": 2,
    },
    {
        "name": "Rogue One: A Star Wars Story",
        "rating": 83.1,
        "duration": datetime.timedelta(minutes=133),
        "director": 4,
        "description": (
            "When she's a child, Jyn's father is forcibly taken by the Empire "
            "to help them complete the Death Star. As an adult, she joins a "
            "group of resistance fighters, who aim to steal its blueprints."
        ),
        "release_date": datetime.date(year=2016, month=12, day=13),
        "oscar_nominations": 2,
        "won_oscar": False,
        "box_office": Decimal("1056.0"),
        "barcode": 6396501778,
        "genre": 2,
    },
    {
        "name": "Star Wars: The Last Jedi",
        "rating": 91.2,
        "duration": datetime.timedelta(minutes=152),
        "director": 7,
        "description": (
            "Rey seeks to learn the ways of the Jedi under Luke Skywalker, "
            "its remaining member, to reinvigorate the Resistance's war "
            "against the First Order."
        ),
        "release_date": datetime.date(year=2017, month=12, day=14),
        "oscar_nominations": 4,
        "won_oscar": False,
        "box_office": Decimal("1333.0"),
        "barcode": 1020122875,
        "genre": 2,
    },
    {
        "name": "Solo: A Star Wars Story",
        "rating": 70.5,
        "duration": datetime.timedelta(minutes=135),
        "director": 8,
        "description": (
            "In a galaxy where hyperfuel is in high demand, Han Solo gets "
            "involved in a large-scale heist within the criminal underworld "
            "and meets individuals who change his life."
        ),
        "release_date": datetime.date(year=2018, month=5, day=25),
        "oscar_nominations": 0,
        "won_oscar": False,
        "box_office": Decimal("393.2"),
        "barcode": 4949091770,
        "genre": 2,
    },
    {
        "name": "Star Wars: The Rise of Skywalker",
        "rating": 54.7,
        "duration": datetime.timedelta(minutes=142),
        "director": 3,
        "description": (
            "The surviving Resistance faces the First Order once more as Rey, "
            "Finn and Poe Dameron's journey continues. With the power and "
            "knowledge of generations behind them, the final battle commences."
        ),
        "release_date": datetime.date(year=2019, month=12, day=19),
        "oscar_nominations": 3,
        "won_oscar": False,
        "box_office": Decimal("1074.0"),
        "barcode": 3592641903,
        "genre": 2,
    },
    {
        "name": "The Lord of the Rings: The Fellowship of the Ring",
        "rating": 91.1,
        "duration": datetime.timedelta(minutes=208),
        "director": 1,
        "description": (
            "A young hobbit, Frodo, who has found the One Ring that belongs "
            "to the Dark Lord Sauron, begins his journey with eight "
            "companions to Mount Doom, the only place where it can be "
            "destroyed."
        ),
        "release_date": datetime.date(year=2001, month=12, day=10),
        "oscar_nominations": 12,
        "won_oscar": True,
        "box_office": Decimal("887.8"),
        "barcode": 9520764061,
        "genre": 1,
    },
    {
        "name": "The Lord of the Rings: The Two Towers",
        "rating": 95.2,
        "duration": datetime.timedelta(minutes=223),
        "director": 1,
        "description": (
            "Frodo and Sam arrive in Mordor with the help of Gollum. A number "
            "of new allies join their former companions to defend Isengard as "
            "Saruman launches an assault on it."
        ),
        "release_date": datetime.date(year=2002, month=12, day=11),
        "oscar_nominations": 6,
        "won_oscar": True,
        "box_office": Decimal("951.2"),
        "barcode": 2545685641,
        "genre": 1,
    },
    {
        "name": "The Lord of the Rings: The Return of the King",
        "rating": 93.0,
        "duration": datetime.timedelta(minutes=201),
        "director": 1,
        "description": (
            "The former Fellowship members prepare for the final battle. "
            "While Frodo and Sam approach Mount Doom to destroy the One Ring, "
            "they follow Gollum unaware of the path he is leading them to."
        ),
        "release_date": datetime.date(year=2003, month=12, day=17),
        "oscar_nominations": 12,
        "won_oscar": True,
        "box_office": Decimal("1142.0"),
        "barcode": 6118332538,
        "genre": 1,
    },
    {
        "name": "The Hobbit: An Unexpected Journey",
        "rating": 64.2,
        "duration": datetime.timedelta(minutes=182),
        "director": 1,
        "description": (
            "Bilbo Baggins, a hobbit, is persuaded into accompanying a wizard "
            "and a group of dwarves on a journey to reclaim the city of "
            "Erebor and all its riches from the dragon Smaug."
        ),
        "release_date": datetime.date(year=2012, month=12, day=12),
        "oscar_nominations": 3,
        "won_oscar": False,
        "box_office": Decimal("1021.0"),
        "barcode": 3604722656,
        "genre": 1,
    },
    {
        "name": "The Hobbit: The Desolation of Smaug",
        "rating": 74.9,
        "duration": datetime.timedelta(minutes=187),
        "director": 1,
        "description": (
            "Bilbo Baggins, a hobbit, and his companions face great dangers "
            "on their journey to Laketown. Soon, they reach the Lonely "
            "Mountain, where Bilbo comes face-to-face with the fearsome "
            "dragon Smaug."
        ),
        "release_date": datetime.date(year=2013, month=12, day=13),
        "oscar_nominations": 3,
        "won_oscar": False,
        "box_office": Decimal("958.0"),
        "barcode": 2522965834,
        "genre": 1,
    },
    {
        "name": "The Hobbit: The Battle of the Five Armies",
        "rating": 59.0,
        "duration": datetime.timedelta(minutes=164),
        "director": 1,
        "description": (
            "Bilbo fights against a number of enemies to save the life of his "
            "Dwarf friends and protects the Lonely Mountain after a conflict "
            "arises."
        ),
        "release_date": datetime.date(year=2014, month=12, day=1),
        "oscar_nominations": 1,
        "won_oscar": False,
        "box_office": Decimal("956.0"),
        "barcode": 3939605744,
        "genre": 2,
    },
]


STUDIOS: t.List[t.Dict[str, t.Any]] = [
    {
        "name": "Shepperton Studios",
        "facilities": {
            "sound_stage": True,
            "catering": True,
            "water_tank": True,
        },
        "description": (
            "Shepperton Studios is a film studio located in Shepperton, "
            "Surrey, England, with a history dating back to 1931. It is now "
            "part of the Pinewood Studios Group. During its early existence, "
            "the studio was branded as Sound City."
        ),
    }
]


TICKETS: t.List[t.Dict[str, t.Any]] = [
    {
        "booked_by": "star_wars_super_fan_1",
        "movie": 1,
        "start_date": datetime.date(year=2022, month=1, day=20),
        "start_time": datetime.time(hour=16, minute=15),
        "booked_on": datetime.datetime(
            year=2022, month=1, day=12, hour=9, minute=30
        ),
    },
    {
        "booked_by": "bilbo_63",
        "movie": 15,
        "start_date": datetime.date(year=2022, month=2, day=22),
        "start_time": datetime.time(hour=19, minute=30),
        "booked_on": datetime.datetime(
            year=2022, month=2, day=11, hour=16, minute=30
        ),
    },
]


SORTED_COLUMNS: t.List[t.Dict[str, t.Any]] = [
    {
        "integer": 5,
        "letter": "a",
    },
    {
        "integer": 2,
        "letter": "b",
    },
    {
        "integer": 3,
        "letter": "c",
    },
    {
        "integer": 7,
        "letter": "b",
    },
    {
        "integer": 1,
        "letter": "b",
    },
    {
        "integer": 1,
        "letter": "a",
    },
]


# Some random words used to generate fake movie names.
MOVIE_WORDS: t.List[str] = [
    "Adventure",
    "Alien",
    "Armageddon",
    "Android",
    "Bridge",
    "Captain",
    "Destruction",
    "Evolution",
    "Extreme",
    "Fantasy",
    "Friend",
    "Galaxy",
    "King",
    "Lord",
    "Master",
    "Max",
    "Mutant",
    "Outpost",
    "Partner",
    "Phantom",
    "Power",
    "Returns",
    "Revenge",
    "Robot",
    "Star",
    "Throne",
    "Thunder",
    "Twin",
]
