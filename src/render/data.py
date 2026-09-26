# ------------------------------------------------------------------------------
# Last.fm
# ------------------------------------------------------------------------------
LASTFM_USER = "renatodinhani"

# ------------------------------------------------------------------------------
# Tags: display names
# ------------------------------------------------------------------------------
T_TODAY = "Today"
T_ALL = "All"
T_FAVORITES = "Favorites"
T_NON_FAVORITES = "Non-Favorites"
T_OTHERS = "Others"
#
T_ROCK_ALL = "Rock"
T_ROCK_FAVORITES = "Rock - Favorites"
T_ROCK_NON_FAVORITES = "Rock - Non-Favorites"
T_ROCK_HEAVY_METAL = "Rock - Heavy Metal"
T_ROCK_FOLK_METAL = "Rock - Folk Metal"
T_ROCK_EXTREME_METAL = "Rock - Extreme Metal"
T_ROCK_ROCK = "Rock - Rock"
#
T_FOLK_ALL = "Folk"
T_FOLK_FAVORITES = "Folk - Favorites"
T_FOLK_NON_FAVORITES = "Folk - Non-Favorites"
T_FOLK_FOLK = "Folk - Folk"
T_FOLK_STEAMPUNK = "Folk - Steampunk"
#
T_ALT_ALL = "Alternative"
T_ALT_FAVORITES = "Alt - Favorites"
T_ALT_NON_FAVORITES = "Alt - Non-Favorites"
T_ALT_ATMOSPHERIC = "Alt - Atmospheric"
T_ALT_ENERGETIC = "Alt - Energetic"
T_ALT_VOICE_GUITAR = "Alt - Vox/Guitar"

# ------------------------------------------------------------------------------
# Tags contains data from other more granular tags
# ------------------------------------------------------------------------------
TAGS_UMBRELLA = [
    T_ALL, T_FAVORITES, T_NON_FAVORITES,
    T_ROCK_ALL, T_ROCK_FAVORITES, T_ROCK_NON_FAVORITES,
    T_FOLK_ALL, T_FOLK_FAVORITES, T_FOLK_NON_FAVORITES,
    T_ALT_ALL, T_ALT_FAVORITES, T_ALT_NON_FAVORITES,
]

# ------------------------------------------------------------------------------
# Tags to be show as header in the menu
# ------------------------------------------------------------------------------
TAGS_HEADER = [
    T_ROCK_ALL,
    T_FOLK_ALL,
    T_ALT_ALL,
]

# ------------------------------------------------------------------------------
# Tags of favorites and non-favorites
# ------------------------------------------------------------------------------
TAGS_FAVORITES = [
    T_ROCK_FAVORITES,
    T_FOLK_FAVORITES,
    T_ALT_FAVORITES,
]

# ------------------------------------------------------------------------------
# Tag order to be displayed in the menu
# ------------------------------------------------------------------------------
TAGS_MENU_ORDER = [
    T_ALL,
    T_FAVORITES,
    T_NON_FAVORITES,
    T_OTHERS,
    #
    # T_ROCK_SEP,
    T_ROCK_ALL,
    T_ROCK_FAVORITES,
    T_ROCK_NON_FAVORITES,
    T_ROCK_HEAVY_METAL,
    T_ROCK_EXTREME_METAL,
    T_ROCK_FOLK_METAL,
    T_ROCK_ROCK,
    #
    T_FOLK_ALL,
    T_FOLK_FAVORITES,
    T_FOLK_NON_FAVORITES,
    T_FOLK_FOLK,
    T_FOLK_STEAMPUNK,
    #
    T_ALT_ALL,
    T_ALT_FAVORITES,
    T_ALT_NON_FAVORITES,
    T_ALT_ATMOSPHERIC,
    T_ALT_ENERGETIC,
    T_ALT_VOICE_GUITAR,
]

# ------------------------------------------------------------------------------
# Mappings
# ------------------------------------------------------------------------------
TAG_RULES = {
    # --------------------------------------------------------------------------
    # Rock / Metal
    # --------------------------------------------------------------------------
    T_ROCK_ALL: [
        T_ROCK_ROCK,
        T_ROCK_EXTREME_METAL,
        T_ROCK_HEAVY_METAL,
        T_ROCK_FOLK_METAL,
    ],
    T_ROCK_FAVORITES: [
        "+Alestorm",
        "+Altaria",
        "+Amorphis",
        "+ANGRA",
        "+Aquaria",
        "+Ayreon",
        "+Crypta",
        "+Doomsword",
        "+Dream Theater",
        "+Eldhrimnir",
        "+Gamma Ray",
        "+Haggard",
        "+Haken",
        "+Hangar",
        "+Iced Earth",
        "+In Mourning",
        "+Judas Priest",
        "+Mägo de Oz",
        "+Narnia",
        "+Oficina G3",
        "+Opeth",
        "+Orphaned Land",
        "+Otyg",
        "+Sabaton",
        "+Satyricon",
        "+Sentenced",
        "+Sepultura",
        "+Shaman",
        "+Sonata Arctica",
        "+Syd Matters",
        "+Therion",
        "+Torture Squad",
        "+Tuatha de Danann",
        "+Týr"
    ],
    T_ROCK_HEAVY_METAL: [
        "-Ahab",
        "-Amon Amarth",
        "-Arch Enemy",
        "-Arcturus",
        "-Death",
        "-Gotthard",
        "-In Mourning",
        "-Scorpions",
        "-Torture Squad",
        "+Massacration",
        "+Stress",
        "-Whitesnake",
        "christian rock",
        "glam metal",
        "gothic metal",
        "heavy metal",
        "nu metal",
        "power metal",
        "progressive metal",
        "thrash metal",
        "doom metal"
    ],
    T_ROCK_FOLK_METAL: [
        "-Amon Amarth",
        "-Amorphis",
        "-Blind Guardian",
        "-Borknagar",
        "-Braia",
        "-HammerFall",
        "-Kamelot",
        "-Leaves' Eyes",
        "-Nightwish",
        "-Rhapsody",
        "-Sabaton",
        "-Sólstafir",
        "-Sonata Arctica",
        "-Ye Banished Privateers",
        "+Diablo Swing Orchestra",
        "folk metal"
    ],
    T_ROCK_EXTREME_METAL: [
        "-Sentenced",
        "-Therion",
        "+Ahab",
        "black metal",
        "death metal",
        "melodic death metal"
    ],
    T_ROCK_ROCK: [
        "-Dio",
        "-Iron Maiden",
        "-Jorn",
        "-Judas Priest",
        "-Metallica",
        "-Ozzy Osbourne",
        "+Barns Courtney",
        "+Boz Scaggs",
        "+Camp Claude",
        "+Creedence Clearwater Revival",
        "+Daughter",
        "+Imagine Dragons",
        "+Kansas",
        "+Lordi",
        "+Poets of the Fall",
        "+Syd Matters",
        "+Tame Impala",
        "+The Dead South",
        "+Wussy",
        "alternative rock",
        "hard rock",
        "post-grunge",
        "rock",
        "shoegaze"
    ],
    # --------------------------------------------------------------------------
    # Folk / Steampunk
    # --------------------------------------------------------------------------
    T_FOLK_ALL: [
        T_FOLK_FOLK,
        T_FOLK_STEAMPUNK
    ],
    T_FOLK_FAVORITES: [
        "-Eluveitie",
        "+Celtic Woman",
        "+Confraria da Costa",
        "+Dirt Poor Robins",
        "+Eldhrimnir",
        "+Eliza Rickman",
        "+Haute & Freddy",
        "+Steam Powered Giraffe",
        "+The Cog is Dead"
    ],
    T_FOLK_FOLK: [
        "-Tuatha de Danann",
        "+Confraria da Costa",
        "+Deolinda",
        "+Eldhrimnir",
        "+Hildegard von Blingin'",
        "+Madredeus",
        "+The Dead South",
        "+Ye Banished Privateers",
        "celtic",
    ],
    T_FOLK_STEAMPUNK: [
        "-Diablo Swing Orchestra",
        "-Leandra",
        "+AlicebanD",
        "+Amanda Palmer",
        "+American Murder Song",
        "+Aurelio Voltaire",
        "+Bitter Ruin",
        "+Dirt Poor Robins",
        "+Eliza Rickman",
        "+Ghost Quartet",
        "+Haute & Freddy",
        "+Kim Tillman",
        "+Major Parkinson",
        "+Steam Powered Giraffe",
        "+The Cog is Dead",
        "+The Dresden Dolls",
        "+Unwoman"
    ],
    # --------------------------------------------------------------------------
    # Alternativo
    # --------------------------------------------------------------------------
    T_ALT_ALL: [
        T_ALT_ATMOSPHERIC,
        T_ALT_ENERGETIC,
        T_ALT_VOICE_GUITAR,
    ],
    T_ALT_FAVORITES: [
        "+aeseaes",
        "+Agnes Obel",
        "+Allie X",
        "+Angus & Julia Stone",
        "+Billie Eilish",
        "+Birdy",
        "+Burning Peacocks",
        "+Chappell Roan",
        "+Daughter",
        "+Dua Lipa",
        "+Eliza Rickman",
        "+Fish in a Birdcage",
        "+Florence + The Machine",
        "+HÆLOS",
        "+Jessie Ware",
        "+Joyce Jonathan",
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
        "+Of Monsters and Men",
        "+Oh Land",
        "+Oh Wonder",
        "+PHILDEL",
        "+Ruelle",
        "+Sabrina Carpenter",
        "+Sia",
        "+Stromae",
        "+Susanne Sundfør",
        "+The Dø",
        "+Vaults",
        "+Zella Day"
    ],
    T_ALT_ATMOSPHERIC: [
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
        "+Lorien Testard",
        "+lùisa",
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
        "+Vaults"
    ],
    T_ALT_ENERGETIC: [
        "+Allie X",
        "+AURORA",
        "+Britney Spears",
        "+BROODS",
        "+Chappell Roan",
        "+Claire Rosinkranz",
        "+Dua Lipa",
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
        "+Of Monsters and Men",
        "+P!nk",
        "+Prudence",
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
        "+Alela Diane",
        "+Angus & Julia Stone",
        "+Billie Marten",
        "+Cocoon",
        "+Fish in a Birdcage",
        "+Frøkedal",
        "+Gabrielle Shonk",
        "+LAUREL",
        "+Marika Hackman",
        "+Michelle Gurevich",
        "+Sidney Gish",
        "+The Staves",
        "indie folk",
    ]
}

from render.utils import ProxyDict
TAGS_BY_RULE = ProxyDict(list)
for tag, patterns in TAG_RULES.items():
    for pattern in patterns:
        TAGS_BY_RULE[pattern].append(tag)
