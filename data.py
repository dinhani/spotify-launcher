# ------------------------------------------------------------------------------
# Tags: display names
# ------------------------------------------------------------------------------
T_ALL = "All"
T_OTHERS = "Others"
#
T_ROCK_SEP = "Header - Rock / Metal"
T_ROCK_ALL = "Rock - All"
T_ROCK_FAVORITES = "Rock - Favorites"
T_ROCK_EXTREME_METAL = "Rock - Extreme Metal"
T_ROCK_HEAVY_METAL = "Rock - Heavy Metal"
T_ROCK_FOLK_METAL = "Rock - Folk Metal"
T_ROCK = "Rock - Rock"
#
T_FOLK_SEP = "Header - Folk"
T_FOLK_ALL = "Folk - All"
T_FOLK_FAVORITES = "Folk - Favorites"
T_FOLK = "Folk - Folk"
T_STEAMPUNK = "Folk - Steampunk"
#
T_ALT_SEP = "Header - Alternative"
T_ALT_ALL = "Alt - All"
T_ALT_FAVORITES = "Alt - Favorites"
T_ALT_ATMOSPHERIC = "Alt - Atmospheric"
T_ALT_ENERGETIC = "Alt - Energetic"
T_ALT_VOICE_GUITAR = "Alt - Vox/Guitar"

# ------------------------------------------------------------------------------
# Tag Order: used in the menu
# ------------------------------------------------------------------------------
TAGS_ORDER = [
    T_ALL,
    T_OTHERS,
    #
    T_ROCK_SEP,
    T_ROCK_ALL,
    T_ROCK_FAVORITES,
    T_ROCK_EXTREME_METAL,
    T_ROCK_HEAVY_METAL,
    T_ROCK_FOLK_METAL,
    T_ROCK,
    #
    T_FOLK_SEP,
    T_FOLK_ALL,
    T_FOLK_FAVORITES,
    T_FOLK,
    T_STEAMPUNK,
    #
    T_ALT_SEP,
    T_ALT_ALL,
    T_ALT_FAVORITES,
    T_ALT_ATMOSPHERIC,
    T_ALT_ENERGETIC,
    T_ALT_VOICE_GUITAR,
]

# ------------------------------------------------------------------------------
# Mappings
# ------------------------------------------------------------------------------
TAGS_INVERTED = {
    # --------------------------------------------------------------------------
    # Rock / Metal
    # --------------------------------------------------------------------------
    T_ROCK_ALL: [
        T_ROCK,
        T_ROCK_EXTREME_METAL,
        T_ROCK_HEAVY_METAL,
        T_ROCK_FOLK_METAL,
    ],
    T_ROCK_FAVORITES: [
        "+Iced Earth",
    ],
    T_ROCK_HEAVY_METAL: [
        "-Gotthard",
        "+Massacration",
        "+Stress",
        "christian rock",
        "glam metal",
        "gothic metal",
        "hard rock",
        "heavy metal",
        "nu metal",
        "power metal",
        "progressive metal",
        "thrash metal",
        "doom metal"
    ],
    T_ROCK_FOLK_METAL: [
        "-Leaves' Eyes",
        "-Nightwish",
        "-Rhapsody",
        "-Sabaton",
        "-Sonata Arctica",
        "folk metal",
        "viking metal"
    ],
    T_ROCK_EXTREME_METAL: [
        "-Therion",
        "black metal",
        "death metal",
        "melodic death metal"
    ],
    T_ROCK: [
        "-Iron Maiden",
        "+Barns Courtney",
        "+Camp Claude",
        "+Daughter",
        "+Imagine Dragons",
        "+Lordi",
        "+Syd Matters",
        "+Tame Impala",
        "+The Dead South",
        "+Wussy",
        "album rock",
        "alternative rock",
        "post-grunge",
        "rock",
        "shoegaze"
    ],
    # --------------------------------------------------------------------------
    # Folk / Steampunk
    # --------------------------------------------------------------------------
    T_FOLK_ALL: [
        T_FOLK,
        T_STEAMPUNK
    ],
    T_FOLK_FAVORITES: [
        "+Eliza Rickman",
        "+Steam Powered Giraffe"
    ],
    T_FOLK: [
        "+Confraria da Costa",
        "+The Dead South",
        "celtic",
    ],
    T_STEAMPUNK: [
        "dark cabaret"
    ],
    # --------------------------------------------------------------------------
    # Alternativo
    # --------------------------------------------------------------------------
    T_ALT_ALL: [
        T_ALT_ATMOSPHERIC,
        T_ALT_ENERGETIC,
        T_ALT_VOICE_GUITAR
    ],
    T_ALT_FAVORITES: [
        "+London Grammar"
    ],
    T_ALT_ATMOSPHERIC: [
        "+aeseaes",
        "+AURORA",
        "+Billie Eilish",
        "+Birdy",
        "+Burning Peacocks",
        "+Cathedrals",
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
        "+Oh Land",
        "+Oh Wonder",
        "+Paris Paloma",
        "+PHILDEL",
        "+Phoebe Bridgers",
        "+Prudence",
        "+Rosemary & Garlic",
        "+Ruelle",
        "+Soap&Skin",
        "+Sóley",
        "+Susanne Sundfør",
        "+The xx",
        "+Vaults",
        "chamber pop"
    ],
    T_ALT_ENERGETIC: [
        "+BROODS",
        "+Claire Rosinkranz",
        "+Jessie Ware",
        "+Joyce Jonathan",
        "+Kaleida",
        "+Lady Gaga",
        "+Las Aves",
        "+LÉON",
        "+Lola Young",
        "+Lorde",
        "+MARINA",
        "+Of Monsters and Men",
        "+Prudence",
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

from dict import ProxyDict
TAGS = ProxyDict()
for tag, patterns in TAGS_INVERTED.items():
    for pattern in patterns:
        TAGS[pattern] = tag