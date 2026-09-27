# Contexto: histórico estendido do Spotify

Arquivo de retomada de sessão. Não commitado.

## Objetivo

Usar o histórico estendido de streams do Spotify (pedido em 2026-09-26, ver "Planned: long-term history" no `AGENTS.md`) em duas frentes:

1. **Análise manual (feita):** cruzar o histórico com os artistas seguidos (`data/artists.tsv`) e achar artistas que ouvi bastante mas não sigo.
2. **Integração no app (pendente):** ver se dá para gerar valor na aplicação com esses dados. Ainda não discutido.

## Dados

- Export bruto: `Z:/pessoal/redes-sociais/spotify-2026-09` (`Streaming_History_Audio_*.json`, `Streaming_History_Video_*.json`, 2015–2026).
- Extração: `just history` → `src/spotify-history.py` → `data/streams.tsv`.
- `data/streams.tsv` está no `.gitignore`: **os dados não são commitados** por enquanto. Só o script, a receita e o `.gitignore` foram commitados.

### Decisões da extração

- Só músicas: podcasts são irrelevantes para o app e ficam de fora. Audiobooks não existem no export.
- Descartados: IP, país, offline, timestamp offline, modo anônimo, texto bruto da plataforma (contém IDs de aparelho).
- Formato TSV, igual a `artists.tsv`. Nome do script `spotify-history`.
- Colunas: `ended_at`, `played_ms`, `artist`, `album`, `track`, `track_id`, `device`, `reason_start`, `reason_end`, `shuffle`, `skipped`, `offline`.
- `ended_at` é o **fim** da reprodução (é o que o `ts` do Spotify significa), ISO 8601 no fuso `America/Sao_Paulo`. Ao ler com polars ele vira UTC; converter de volta para análises por hora/dia.
- `device` é o texto de plataforma reduzido a `desktop`/`phone`/`tablet`/`speaker`/`tv`/`unknown`.
- `artist` é o artista do álbum; não há ID de artista no export. Cruzamento com os seguidos é por nome (casefold). Participações e coletâneas não contam para o artista.

Números: 95.892 faixas, ~4.840h, 6.151 artistas, 27.586 faixas distintas, 2015-03-01 a 2026-09-25.

## Frente 1: resultado

Os artistas seguidos batem todos com o histórico. Mediana dos seguidos: 7,8h ouvidas (p25 3,7h, p10 2,0h). O não seguido mais ouvido tem 7,4h: o topo de audição já está todo no app. Sobram artistas de 2–7h com audição consistente.

Métricas usadas por artista (só não seguidos, ≥ 1h): horas, faixas distintas com ≥ 30s, reproduções escolhidas (`reason_start` em `clickrow`/`playbtn`), período, anos com audição, faixa mais ouvida e sua fatia do tempo, ano de pico.

### Candidatos fortes (horas, faixas, período)

**Rock:** Epica (6.3, 41, 2016–2026), Katatonia (5.1, 44, 2016–2025), Nevermore (4.1, 29, 2020–2026), Cradle Of Filth (4.0, 14, 2017–2026), Vader (3.8, 25, 2020–2025), Sinergy (3.2, 11, 2018–2026), Dragonheart (2.9, 11, 2016–2021), Evergrey (2.8, 17, 2021–2026), Metsatöll (2.6, 27, 2016–2024), Rosa de Saron (2.6, 17, 2017–2024), In Flames (2.5, 14, 2017–2026), Kreator (2.4, 10, 2020–2026).

**Folk:** O Bardo E O Banjo (7.4, 40, 2019–2025), Abney Park (5.3, 45, 2017–2026), Ghostfire (3.0, 9, 2017–2026), Eivør (2.8, 15, 2019–2026), Charming Disaster (2.5, 13, 2021–2026), Bear Ghost (2.4, 17, 2019–2024), Hillbilly Rawhide (2.3, 41, 2019–2026), Sunday Driver (2.3, 28, 2017–2024).

**Alternative:** CLOVES (7.1, 34, 2017–2023), Adna (6.8, 41, 2017–2023), Sin Fang (5.4, 15, 2018–2026), Warpaint (5.3, 30, 2017–2025), Elsiane (4.9, 18, 2018–2026), Wolf Alice (4.7, 38, 2019–2026), Hozier (4.7, 41, 2017–2026), Girls In Hawaii (4.2, 35, 2022–2025), Jill Andrews (3.8, 23, 2017–2025), Aldous Harding (3.8, 28, 2017–2025), Moriarty (3.7, 32, 2016–2024), Siv Jakobsen (3.6, 31, 2017–2025), Blanco White (3.5, 21, 2018–2026), Novo Amor (3.5, 29, 2017–2025), RHODES (3.5, 22, 2017–2026), La Femme (3.2, 18, 2018–2025), MS MR (3.1, 11, 2017–2026), The Family Crest (3.1, 13, 2020–2026), Laura Marling (2.8, 14, 2017–2025), The National (2.7, 26, 2017–2025), RY X (2.6, 23, 2017–2025), Still Corners (2.5, 16, 2021–2026).

### Segunda linha (1,7–2,4h, espalhado em várias faixas)

- Rock: Detonator, Theatre Of Tragedy, Mono Inc., Triosphere, Dimmu Borgir, Equilibrium, Ensiferum, Eternal Tears Of Sorrow, Candlemass, Alcest, Empyrium, Cellar Darling, Kalandra, Accept, Slipknot, Ghost.
- Folk: Beltaine, Johnny Hollow, This Way To The Egress, The Amazing Devil, Kiki Rockwell.
- Alternative: Bat For Lashes, Fink, Meimuna, Mogli, machineheart, VÉRITÉ, Mree, SYML, Vian Izak, The Woodlands, Yael Naim, Kid Francescoli, José González.

### Descartados

- Uma música só (> 60% do tempo numa faixa): Disclosure, Monkey3, Dion, Charon, Evergreen Terrace, Behemoth, Enslaved, Grave Digger, Bing Crosby, Ben Howard, Silly Boy Blue.
- Surto de um ano só: Lea Lu (4,8h, tudo em 2023), OLI, Clairity, GERD, Nanna Øland Fabricius.
- Trilha sonora ou infantil: Arcane, Mundo Bita, Kero Kero Bonito (pico foi a trilha do Bugsnax), Rich Shapero, Darren Korb.

### Próximo passo da frente 1

Eu decidir quais seguir no Spotify; depois `just download`, `just export`, `just render` e classificar os novos em `TAG_RULES`.

### Script da análise

```python
import polars as pl

h = pl.read_csv("data/streams.tsv", separator="\t", try_parse_dates=True).with_columns(
    pl.col("ended_at").dt.convert_time_zone("America/Sao_Paulo"),
    year=pl.col("ended_at").dt.convert_time_zone("America/Sao_Paulo").dt.year(),
)
followed = [name.casefold() for name in pl.read_csv("data/artists.tsv", separator="\t")["name"]]
h = h.filter(~pl.col("artist").str.to_lowercase().is_in(followed))
top_track = h.group_by("artist", "track").agg(ms=pl.col("played_ms").sum()).sort("ms", descending=True).group_by("artist", maintain_order=True).first()
peak = (
    h.group_by("artist", "year").agg(ms=pl.col("played_ms").sum()).sort("ms", descending=True)
    .group_by("artist", maintain_order=True).first()
    .select("artist", peak_year="year", peak_h=(pl.col("ms") / 3.6e6).round(1))
)
unfollowed = (
    h.group_by("artist").agg(
        hours=(pl.col("played_ms").sum() / 3.6e6).round(1),
        tracks=pl.col("track_id").filter(pl.col("played_ms") >= 30000).n_unique(),
        chosen=pl.col("reason_start").is_in(["clickrow", "playbtn"]).filter(pl.col("played_ms") >= 30000).sum(),
        span=pl.format("{}-{}", pl.col("year").min(), pl.col("year").max()),
        years=pl.col("year").filter(pl.col("played_ms") >= 30000).n_unique(),
        total_ms=pl.col("played_ms").sum(),
    )
    .filter(pl.col("hours") >= 1.0)
    .join(top_track, on="artist").join(peak, on="artist")
    .with_columns(top_share=(pl.col("ms") / pl.col("total_ms") * 100).round(0))
    .drop("ms", "total_ms")
    .sort("hours", descending=True)
)
```

## Frente 2: pendente

Integrar o histórico ao app. O `AGENTS.md` já previa: agregar por artista (tempo ouvido, última vez ouvido) em `data/` e commitar só o agregado. Lembrar que Last.fm (`just lastfm`) só cobre o recente; o histórico do Spotify cobre 2015–2026. Nada decidido ainda: discutir antes de implementar.
