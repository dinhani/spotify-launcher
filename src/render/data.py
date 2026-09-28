from render.models import Family, Tag
from render.utils import TrackedDict

# ------------------------------------------------------------------------------
# Last.fm
# ------------------------------------------------------------------------------
LASTFM_USER = "renatodinhani"

# ------------------------------------------------------------------------------
# Tags
# ------------------------------------------------------------------------------
T_ALL = Tag("All", "🗂️")
T_DISCOVER = Tag("Discover", "")
T_FAVORITES = Tag("Favorites", "")
T_NON_FAVORITES = Tag("Non-Favorites", "")
T_OTHERS = Tag("Others", "🎶", "Fits no style, mostly instrumental")
#
T_ROCK_ALL = Tag("Rock", "🎸", "Metal and rock")
T_ROCK_DISCOVER = Tag("Rock - Discover", "")
T_ROCK_FAVORITES = Tag("Rock - Favorites", "")
T_ROCK_NON_FAVORITES = Tag("Rock - Non-Favorites", "")
T_ROCK_HEAVY_METAL = Tag("Rock - Heavy Metal", "", "Power, progressive, thrash, gothic")
T_ROCK_FOLK_METAL = Tag("Rock - Folk Metal", "", "Metal with folk, celtic or medieval elements")
T_ROCK_EXTREME_METAL = Tag("Rock - Extreme Metal", "", "Death, black, doom")
T_ROCK_ROCK = Tag("Rock - Rock", "", "Rock without metal: classic, hard, grunge, indie")
#
T_FOLK_ALL = Tag("Folk", "🎻", "Traditional music and theatrical songs")
T_FOLK_DISCOVER = Tag("Folk - Discover", "")
T_FOLK_FAVORITES = Tag("Folk - Favorites", "")
T_FOLK_NON_FAVORITES = Tag("Folk - Non-Favorites", "")
T_FOLK_FOLK = Tag("Folk - Folk", "", "Celtic, medieval, fado, bluegrass, shanties")
T_FOLK_STEAMPUNK = Tag("Folk - Steampunk", "", "Steampunk and dark cabaret")
#
T_ALT_ALL = Tag("Alt & Pop", "🎤", "Indie, electronic, singer-songwriters and pop")
T_ALT_DISCOVER = Tag("Alt - Discover", "")
T_ALT_FAVORITES = Tag("Alt - Favorites", "")
T_ALT_NON_FAVORITES = Tag("Alt - Non-Favorites", "")
T_ALT_ATMOSPHERIC = Tag("Alt - Atmospheric", "", "Layered: strings, electronics, ambience")
T_ALT_ENERGETIC = Tag("Alt - Energetic", "", "Upbeat, danceable")
T_ALT_VOICE_GUITAR = Tag("Alt - Vox/Guitar", "", "Voice with guitar or piano")

# ------------------------------------------------------------------------------
# Families
# ------------------------------------------------------------------------------
FAMILY_ROCK = Family(
    tag=T_ROCK_ALL,
    discover=T_ROCK_DISCOVER,
    favorites=T_ROCK_FAVORITES,
    non_favorites=T_ROCK_NON_FAVORITES,
    granular=(T_ROCK_HEAVY_METAL, T_ROCK_EXTREME_METAL, T_ROCK_FOLK_METAL, T_ROCK_ROCK),
)
FAMILY_FOLK = Family(
    tag=T_FOLK_ALL,
    discover=T_FOLK_DISCOVER,
    favorites=T_FOLK_FAVORITES,
    non_favorites=T_FOLK_NON_FAVORITES,
    granular=(T_FOLK_FOLK, T_FOLK_STEAMPUNK),
)
FAMILY_ALT = Family(
    tag=T_ALT_ALL,
    discover=T_ALT_DISCOVER,
    favorites=T_ALT_FAVORITES,
    non_favorites=T_ALT_NON_FAVORITES,
    granular=(T_ALT_ATMOSPHERIC, T_ALT_ENERGETIC, T_ALT_VOICE_GUITAR),
)
FAMILIES = [FAMILY_ROCK, FAMILY_FOLK, FAMILY_ALT]

# Exclude artists in these families from the corresponding Discover pool.
FAMILY_DISCOVER_EXCLUSIONS = {
    FAMILY_FOLK: [FAMILY_ROCK, FAMILY_ALT],
}

def find_family(tag: Tag) -> Family | None:
    return next((family for family in FAMILIES if tag in family.tags_menu), None)

# ------------------------------------------------------------------------------
# Tags contains data from other more granular tags
# ------------------------------------------------------------------------------
TAGS_UMBRELLA = [
    T_ALL, T_DISCOVER, T_FAVORITES, T_NON_FAVORITES,
    *(tag for family in FAMILIES for tag in family.tags_umbrella),
]

# ------------------------------------------------------------------------------
# Tags to be show as header in the menu
# ------------------------------------------------------------------------------
TAGS_HEADER = [T_ALL, *(family.tag for family in FAMILIES), T_OTHERS]

# ------------------------------------------------------------------------------
# Tag order to be displayed in the menu
# ------------------------------------------------------------------------------
TAGS_MENU_ORDER = [
    T_ALL,
    T_DISCOVER,
    T_FAVORITES,
    T_NON_FAVORITES,
    *(tag for family in FAMILIES for tag in family.tags_menu),
    T_OTHERS,
]

# ------------------------------------------------------------------------------
# Mappings
# ------------------------------------------------------------------------------
TAG_RULES = {
    # --------------------------------------------------------------------------
    # Favorites
    # --------------------------------------------------------------------------
    T_FAVORITES: [
        "-Eluveitie",
        "+aeseaes",
        "+Agnes Obel",
        "+Alestorm",
        "+Allie X",
        "+Altaria",
        "+Amorphis",
        "+ANGRA",
        "+Angus & Julia Stone",
        "+Aquaria",
        "+Ayreon",
        "+Billie Eilish",
        "+Birdy",
        "+Burning Peacocks",
        "+Celtic Woman",
        "+Chappell Roan",
        "+Confraria da Costa",
        "+Crypta",
        "+Daughter",
        "+Dirt Poor Robins",
        "+Doomsword",
        "+Dream Theater",
        "+Dua Lipa",
        "+Eldhrimnir",
        "+Eliza Rickman",
        "+Fish in a Birdcage",
        "+Florence + The Machine",
        "+Gamma Ray",
        "+Haggard",
        "+Haken",
        "+Hangar",
        "+Haute & Freddy",
        "+HÆLOS",
        "+Iced Earth",
        "+In Mourning",
        "+Jessie Ware",
        "+Joyce Jonathan",
        "+Judas Priest",
        "+Juniper Vale",
        "+Lady Gaga",
        "+Las Aves",
        "+Leandra",
        "+London Grammar",
        "+Lor",
        "+Lorde",
        "+Lorien Testard",
        "+lùisa",
        "+Marika Hackman",
        "+MARINA",
        "+Mägo de Oz",
        "+Narnia",
        "+Of Monsters and Men",
        "+Oficina G3",
        "+Oh Land",
        "+Oh Wonder",
        "+Opeth",
        "+Orphaned Land",
        "+Otyg",
        "+PHILDEL",
        "+Ruelle",
        "+Sabaton",
        "+Sabrina Carpenter",
        "+Satyricon",
        "+Sentenced",
        "+Sepultura",
        "+Shaman",
        "+Sia",
        "+Sonata Arctica",
        "+Steam Powered Giraffe",
        "+Stromae",
        "+Susanne Sundfør",
        "+Syd Matters",
        "+The Cog is Dead",
        "+The Dø",
        "+Therion",
        "+Torture Squad",
        "+Tuatha de Danann",
        "+Týr",
        "+Vaults",
        "+Zella Day"
    ],
    # --------------------------------------------------------------------------
    # Rock / Metal
    # --------------------------------------------------------------------------
    T_ROCK_ALL: [
        T_ROCK_ROCK,
        T_ROCK_EXTREME_METAL,
        T_ROCK_HEAVY_METAL,
        T_ROCK_FOLK_METAL,
    ],
    T_ROCK_HEAVY_METAL: [
        "-Ahab",
        "-Amon Amarth",
        "-Arch Enemy",
        "-Arcturus",
        "-Carcass",
        "-Cradle Of Filth",
        "-Death",
        "-Gotthard",
        "-In Mourning",
        "-Poison",
        "-Scorpions",
        "-Torture Squad",
        "-Vader",
        "+Detonator",
        "+Massacration",
        "+Rata Blanca",
        "+Stress",
        "+Sólstafir",
        "+Volbeat",
        "-Whitesnake",
        "christian rock",
        "glam metal",
        "gothic metal",
        "heavy metal",
        "industrial metal",
        "nu metal",
        "power metal",
        "progressive metal",
        "thrash metal",
        "doom metal",
    ],
    T_ROCK_FOLK_METAL: [
        "-Amon Amarth",
        "-Amorphis",
        "-Blind Guardian",
        "-Borknagar",
        "-Braia",
        "-Eldhrimnir",
        "-Epica",
        "-Faun",
        "-HammerFall",
        "-Kamelot",
        "-Leaves' Eyes",
        "-Nightwish",
        "-OMNIA",
        "-Orden Ogan",
        "-Rhapsody",
        "-Rhapsody Of Fire",
        "-Sabaton",
        "-Sólstafir",
        "-Sonata Arctica",
        "-Van Canto",
        "-Wintersun",
        "-Ye Banished Privateers",
        "+Diablo Swing Orchestra",
        "+Suldusk",
        "folk metal",
    ],
    T_ROCK_EXTREME_METAL: [
        "-Sentenced",
        "-Sinergy",
        "-Sólstafir",
        "-Therion",
        "+Ahab",
        "black metal",
        "death metal",
        "melodic death metal",
    ],
    T_ROCK_ROCK: [
        "-Dio",
        "-Iron Maiden",
        "-Jorn",
        "-Judas Priest",
        "-Metallica",
        "-Ozzy Osbourne",
        "-Queensrÿche",
        "+Barns Courtney",
        "+Boz Scaggs",
        "+Camp Claude",
        "+CPM 22",
        "+Creedence Clearwater Revival",
        "+Daughter",
        "+Imagine Dragons",
        "+Kansas",
        "+Lordi",
        "+Poets of the Fall",
        "+Poison",
        "+Syd Matters",
        "+Tame Impala",
        "+Wussy",
        "alternative rock",
        "hard rock",
        "post-grunge",
        "rock",
        "shoegaze",
    ],
    # --------------------------------------------------------------------------
    # Folk / Steampunk
    # --------------------------------------------------------------------------
    T_FOLK_ALL: [
        T_FOLK_FOLK,
        T_FOLK_STEAMPUNK
    ],
    T_FOLK_FOLK: [
        "-ERA",
        "-Tuatha de Danann",
        "+Confraria da Costa",
        "+Deolinda",
        "+Eldhrimnir",
        "+Hildegard von Blingin'",
        "+Madredeus",
        "+O Bardo E O Banjo",
        "+The Dead South",
        "+Ye Banished Privateers",
        "celtic",
    ],
    T_FOLK_STEAMPUNK: [
        "-Diablo Swing Orchestra",
        "-Leandra",
        "+Abney Park",
        "+AlicebanD",
        "+Amanda Palmer",
        "+American Murder Song",
        "+Aurelio Voltaire",
        "+Bitter Ruin",
        "+Dirt Poor Robins",
        "+Eliza Rickman",
        "+Ghost Quartet",
        "+Kim Tillman",
        "+Major Parkinson",
        "+Steam Powered Giraffe",
        "+The Cog is Dead",
        "+The Dresden Dolls",
        "+Unwoman",
    ],
    # --------------------------------------------------------------------------
    # Alt & Pop
    # --------------------------------------------------------------------------
    T_ALT_ALL: [
        T_ALT_ATMOSPHERIC,
        T_ALT_ENERGETIC,
        T_ALT_VOICE_GUITAR,
    ],
    T_ALT_ATMOSPHERIC: [
        "+Elsiane",
        "+ERA",
        "+Girls In Hawaii",
        "+Klergy",
        "+aeseaes",
        "+Agnes Obel",
        "+Anastasia Minster",
        "+AURORA",
        "+Billie Eilish",
        "+Birdy",
        "+Burning Peacocks",
        "+Cathedrals",
        "+Chappell Roan",
        "+Daughter",
        "+Ex:Re",
        "+Gemma Hayes",
        "+HÆLOS",
        "+Jeanne Added",
        "+Juniper Vale",
        "+Lana Del Rey",
        "+Leandra",
        "+London Grammar",
        "+Lor",
        "+lùisa",
        "+MS MR",
        "+Oh Land",
        "+Oh Wonder",
        "+Paris Paloma",
        "+PHILDEL",
        "+Phoebe Bridgers",
        "+Prudence",
        "+Rosemary & Garlic",
        "+Röyksopp",
        "+Ruelle",
        "+Soap&Skin",
        "+Sóley",
        "+Susanne Sundfør",
        "+The xx",
        "+Vaults",
        "+Warpaint",
    ],
    T_ALT_ENERGETIC: [
        "+Addison Rae",
        "+Allie X",
        "+AURORA",
        "+Britney Spears",
        "+BROODS",
        "+Chappell Roan",
        "+Claire Rosinkranz",
        "+Dua Lipa",
        "+Haute & Freddy",
        "+Jessie Ware",
        "+Joyce Jonathan",
        "+Kaleida",
        "+King Princess",
        "+Lady Gaga",
        "+Las Aves",
        "+LÉON",
        "+Lola Young",
        "+Lorde",
        "+Madonna",
        "+MARINA",
        "+Miley Cyrus",
        "+Of Monsters and Men",
        "+P!nk",
        "+Prudence",
        "+RAYE",
        "+Robyn",
        "+Röyksopp",
        "+Sabrina Carpenter",
        "+Sia",
        "+Stromae",
        "+Superorganism",
        "+Susanne Sundfør",
        "+The Dø",
        "+Zella Day",
        "baroque pop",
        "electroclash",
        "eurodance",
        "synthpop",
    ],
    T_ALT_VOICE_GUITAR: [
        "-Of Monsters and Men",
        "+Adna",
        "+Alela Diane",
        "+Angus & Julia Stone",
        "+Billie Marten",
        "+CLOVES",
        "+Cocoon",
        "+Fish in a Birdcage",
        "+Frøkedal",
        "+Gabrielle Shonk",
        "+Jill Andrews",
        "+LAUREL",
        "+Marika Hackman",
        "+Michelle Gurevich",
        "+Sidney Gish",
        "+The Staves",
        "indie folk",
    ]
}

TAGS_BY_RULE: TrackedDict[str | Tag, list[Tag]] = TrackedDict(list)
for tag, patterns in TAG_RULES.items():
    for pattern in patterns:
        TAGS_BY_RULE[pattern].append(tag)
