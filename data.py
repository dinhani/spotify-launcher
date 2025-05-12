import logging

# ------------------------------------------------------------------------------
# Tags: display names
# ------------------------------------------------------------------------------
T_ALT_ATMOSPHERIC = "Atmospheric"
T_ALT_ENERGITIC = "Energetic"
T_ALT_VOICE_GUITAR = "Vox/Guitar"
T_FOLK = "Folk"
T_INDIE = "Indie"
T_METAL_EXTREME = "Extreme Metal"
T_METAL_ALL = "Metal (All)"
T_METAL_TRADITIONAL = "Traditional Metal"
T_OTHERS = "Others"
T_ROCK = "Rock"
T_STEAMPUNK = "Steampunk"
T_ALL = "All"

# ------------------------------------------------------------------------------
# Tag Order: used in the menu
# ------------------------------------------------------------------------------
TAGS_ORDER = [
    T_ALL,
    T_METAL_TRADITIONAL,
    T_METAL_EXTREME,
    T_ROCK,
    T_FOLK,
    T_STEAMPUNK,
    T_ALT_ATMOSPHERIC,
    T_ALT_VOICE_GUITAR,
    T_ALT_ENERGITIC,
    T_OTHERS
]

# ------------------------------------------------------------------------------
# Mappings
# ------------------------------------------------------------------------------
TAGS_INVERTED = {
    # --------------------------------------------------------------------------
    # Metal
    # --------------------------------------------------------------------------
    T_METAL_TRADITIONAL: [
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
    T_METAL_EXTREME: [
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
    T_FOLK: [
        "-Leaves' Eyes",
        "-Nightwish",
        "-Rhapsody",
        "-Sabaton",
        "-Sonata Arctica",
        "+Confraria da Costa",
        "+The Dead South",
        "celtic",
        "folk metal",
        "viking metal"
    ],
    T_STEAMPUNK: [
        "dark cabaret"
    ],
    # --------------------------------------------------------------------------
    # Alternativo
    # --------------------------------------------------------------------------
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
    T_ALT_ENERGITIC: [
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

TAGS = {}
for tag, patterns in TAGS_INVERTED.items():
    for pattern in patterns:
        TAGS[pattern] = tag