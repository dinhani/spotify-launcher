# ------------------------------------------------------------------------------
# Mappings
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

TAGS_ORDER = [
    T_METAL_TRADICIONAL,
    T_METAL_EXTREMO,
    T_FOLK,
    T_ROCK,
    T_STEAMPUNK,
    T_ALT_ATMOSFERICO,
    T_ALT_VOZ,
    T_ALT_ENERGICO,
    T_OUTROS
]

TAGS_INVERTED = {
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
    T_ROCK: [
        "+Camp Claude",
        "-Iron Maiden",
        "+Barns Courtney",
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
    T_STEAMPUNK: [
        "dark cabaret"
    ],
    T_ALT_ATMOSFERICO: [
        "+AURORA",
        "+Gemma Hayes",
        "+aeseaes",
        "+Billie Eilish",
        "+Birdy",
        "+Cathedrals",
        "+Daughter",
        "+Ex:Re",
        "+HÆLOS",
        "+Jeanne Added",
        "+Juniper Vale",
        "+Lana Del Rey",
        "+Leandra",
        "+London Grammar",
        "+Lor",
        "+Oh Land",
        "+Oh Wonder",
        "+Prudence",
        "+PHILDEL",
        "+Phoebe Bridgers",
        "+Rosemary & Garlic",
        "+Ruelle",
        "+Soap&Skin",
        "+Sóley",
        "+Susanne Sundfør",
        "+The xx",
        "+Vaults",
        "+Burning Peacocks",
        "chamber pop"
    ],
    T_ALT_ENERGICO: [
        "+Claire Rosinkranz",
        "+BROODS",
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
        "+Gabrielle Shonk",
        "+LAUREL",
        "+Marika Hackman",
        "+Michelle Gurevich",
        "+Sidney Gish",
        "+Frøkedal",
        "+The Staves",
        "indie folk",
    ]
}
TAGS = {}
for tag, patterns in TAGS_INVERTED.items():
    for pattern in patterns:
        TAGS[pattern] = tag

# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from collections import defaultdict
from dominate.tags import *
from millify import millify
import polars


# ------------------------------------------------------------------------------
# Parse artists tags
# ------------------------------------------------------------------------------
artists_by_tag = defaultdict(list)

artists_df = polars.read_csv("data/artistas.tsv", separator="\t")
for artist in artists_df.to_dicts():
    # parse row
    tags = set()
    genres = artist["genres"]
    if genres is None:
        genres = []
    else:
        genres = genres.split("|")

    # match genres
    for tag in genres:
        tag = TAGS.get(tag)
        if tag:
            tags.add(tag)

    # match names (positive)
    tag = TAGS.get(f"+{artist["name"]}")
    if tag:
        tags.add(tag)

    # match names (negative)
    tag = TAGS.get(f"-{artist["name"]}")
    if tag:
        tags.remove(tag)

    # specific rules
    if T_METAL_EXTREMO in tags and T_METAL_TRADICIONAL in tags:
        tags.remove(T_METAL_TRADICIONAL)
    if T_METAL_TRADICIONAL in tags or T_METAL_EXTREMO in tags:
        tags.add(T_METAL_TODOS)

    # add tags
    artist["tags"] = tags
    for tag in artist["tags"]:
        artists_by_tag[tag].append(artist)
    if len(artist["tags"]) == 0:
        artists_by_tag[T_OUTROS].append(artist)

# ------------------------------------------------------------------------------
# Generate HTML
# ------------------------------------------------------------------------------

JS_SORT_FUNCTION = """
function sort(button, attribute, order) {
    $(button).addClass('active');
    $(button).siblings().removeClass('active');
    $('.artists').each(function(_, artists) {
        var sorted = $(artists).find('.artist').sort(function(a, b) {
            var valA = $(a).data(attribute);
            var valB = $(b).data(attribute);

            // Check if the values are numeric
            if ($.isNumeric(valA)) {
                return order === 'asc' ? valA - valB : valB - valA; // Numeric comparison
            } else {
                return order === 'asc' ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA)); // String comparison
            }
        });
        $(artists).empty().append(sorted);
    });
}
"""

def menu_categories():
    with div(cls="ui fluid vertical menu"):
        for i, tag in enumerate(TAGS_ORDER):
            artists = artists_by_tag[tag]
            active = "active" if i == 0 else ""
            with div(cls=f"{active} item", data_tab=tab_id(tag)):
                span(f"{len(artists):02}", cls="ui tiny label")
                span(tag)

def menu_sort():
    with div(cls="ui fluid vertical menu"):
        div("🎶 Nome", cls="ui active item", onClick="sort(this, 'name', 'asc')")
        div("👤 Seguidores", cls="ui item", onClick="sort(this, 'followers', 'desc')")
        div("🔥 Popularidade", cls="ui item", onClick="sort(this, 'popularity', 'desc')")
        div("💿 Discos", cls="ui item", onClick="sort(this, 'albums', 'desc')")


def cards(artists: list[dict]):
    # scroll
    with div(style="height: 98vh; overflow-y: scroll;"):
        # grid
        with div(cls="ui padded grid artists"):
            # cards
            for artist in artists:
                followers_precision = 1 if artist["followers.total"] >= 1_000_000 else 0

                with div(cls="ui eight wide mobile two wide computer column artist", style="padding: 0.25rem;", data_name=artist["name"], data_followers=str(artist["followers.total"]), data_popularity=str(artist["popularity"]), data_albums=str(artist["album_count"])):
                    with a(cls="ui card", href=f"spotify:artist:{artist["id"]}", style="width: 100%"):
                        # image
                        with div(cls="image"):
                            img(src=artist["image"], cls="ui image", style="height: 140px; object-fit: cover;")

                        # header
                        with div(cls="content", style="padding: 0.5rem;"):
                            div(artist["name"], cls="ui small header", style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;")

                        # footer
                        with div(cls="extra content", style="padding: 0.5rem;"):
                            span("👤" + millify(artist["followers.total"], precision=followers_precision))
                            span("🔥" + str(artist["popularity"]))
                            span("💿" + str(artist["album_count"]))


def tab_id(tag: str) -> str:
    id = tag.lower().replace("(", "").replace(")", "").replace(":", "").replace(" ", "-").translate(str.maketrans("ãéó", "aeo"))
    return f"tab-{id}"

doc = html(style="height:100%;")
with doc:
    # head
    with head():
        script(src = "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
        script(src = "https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
        script(src = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.js")
        link(href =  "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.css", rel = "stylesheet")

        script(JS_SORT_FUNCTION)

    # body
    with body(cls="ui fluid container", style="height:100%; overflow-y: hidden;"):
        with div(cls="ui padded grid"):
            # ------------------------------------------------------------------
            # Menu
            # ------------------------------------------------------------------
            with div(cls="ui sixteen wide mobile two wide computer column", style="padding: 0.5rem"):
                menu_categories()
                menu_sort()

            # ------------------------------------------------------------------
            # Content
            # ------------------------------------------------------------------
            with div(cls="ui sixteen wide mobile fourteen wide computer column", style="padding: 0.5rem;"):
                # tab contents
                for tag in TAGS_ORDER:
                    artists = sorted(artists_by_tag[tag], key=lambda x: x["name"].lower())
                    active = "active" if i == 0 else ""

                    with div(cls="ui tab", data_tab=tab_id(tag)):
                        cards(artists)

    # script
    script("$('.menu .item').tab({history:true, historyType: 'hash'});")
    script("$('.ui.rating').rating();")

# write to file
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(str(doc))

# write summary
with open("docs/classificao.txt", "w", encoding="utf-8") as f:
    for tag in TAGS_ORDER:
        f.write("\n")
        f.write(tag + ":\n")
        for artist in artists_by_tag[tag]:
            f.write("* " + artist["name"] + "\n")