# -- LIBRARIES ---
library(data.table)
library(tidyverse)
options(scipen = 999)

# -- READ DATA ---
artists <- fread("../data/artists.tsv")
streams <- fread("../data/streams.tsv") |>
  arrange(ended_at) |>
  mutate(
    following = str_to_lower(artist) %in% str_to_lower(artists$name),
  )

# -- ANALYSE DATA ---
streams |>
  filter(!following) |> 
  group_by(artist, track, following) |>
  summarise(
    plays = n(),
    songs = unique(track) |> length(),
    hours = sum(played_ms) / 3.6e6
  ) |>
  arrange(desc(plays)) |> 
  View("Spotify Streams")
