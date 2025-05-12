import logging

# ------------------------------------------------------------------------------
# Tags: display names
# ------------------------------------------------------------------------------
T_ALT_ATMOSFERICO = "Alt: Atmosférico"
T_ALT_ENERGICO = "Alt: Enérgico"
T_ALT_VOZ = "Alt: Voz & Violão"
T_FOLK = "Folclórico"
T_INDIE = "Indie"
T_METAL_TODOS = "Metal (todos)"
T_METAL_EXTREMO = "Metal Extremo"
T_METAL_TRADICIONAL  = "Metal Tradicional"
T_OUTROS = "Outros"
T_ROCK = "Rock"
T_STEAMPUNK = "Steampunk"

# ------------------------------------------------------------------------------
# Tag Order: used in the menu
# ------------------------------------------------------------------------------
TAGS_ORDER = [
    T_METAL_TRADICIONAL,
    T_METAL_EXTREMO,
    T_ROCK,
    T_FOLK,
    T_STEAMPUNK,
    T_ALT_ATMOSFERICO,
    T_ALT_VOZ,
    T_ALT_ENERGICO,
    T_OUTROS
]

# ------------------------------------------------------------------------------
# Mappings
# ------------------------------------------------------------------------------
TAGS_INVERTED = {
    # --------------------------------------------------------------------------
    # Metal
    # --------------------------------------------------------------------------
    T_METAL_TRADICIONAL: [
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
    T_METAL_EXTREMO: [
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
    T_ALT_ATMOSFERICO: [
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
    T_ALT_ENERGICO: [
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
    T_ALT_VOZ: [
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