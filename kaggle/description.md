# GTA 6 Launch Night on Kick.com — Hourly Viewership

> ### Collected with the Kick Scraper on Apify
> **https://apify.com/bhole_krishna/kick-scraper**
>
> Every row here came from that actor. Kick keeps no history, so the hours after this dataset
> ends can only be obtained by collecting them live — point the actor at any category, put it on
> an hourly schedule, and you are building the same record for whatever launches next. It also
> returns past broadcasts with working VOD links, most-viewed clips, channel profiles, and all
> 18,000+ Kick categories ranked by live viewers.

## Why this dataset exists

Kick.com publishes only the present moment. Its public API will tell you how many people are
watching a category *right now*, and nothing about any earlier instant. There is no history
endpoint and no archive. The platform did not keep the hour-by-hour shape of the biggest game
launch in history as it happened on Kick — so it had to be recorded live, or not at all.

This is that recording: 22 hourly snapshots of Kick.com through the GTA 6 launch, 18–19 November
2026 (UTC).

## The headline

| | |
|---|---|
| **Start** | 7,905 concurrent viewers — 13th most-watched category (18 Nov, 08:30 UTC) |
| **Peak** | **1,353,198** concurrent viewers — 1st (18 Nov, 23:30 UTC) |
| **Growth** | 171x in 15 hours |
| **Steepest climb** | +1,132,698 viewers in two hours (09:30 to 11:30 UTC) |
| **Biggest single stream** | RRaenee, 271,680 concurrent viewers |
| **Live GTA 6 streams at once** | up to 899 |
| **Leading language** | **Arabic**, ahead of Portuguese, Turkish and English |

That last row is the one most likely to surprise you. Measured in viewer-hours across the launch,
GTA 6 on Kick was a bigger Arabic-language and Portuguese-language event than an English-language
one.

## Files

**`gta6_viewers_hourly.csv`** (23 rows) — the headline series. One row per snapshot, with GTA 6's
concurrent viewers and rank, plus Just Chatting, IRL, GTA V and Slots read at the same instant and
the sum of the 30 largest categories for platform-wide scale.

**`gta6_streams_hourly.csv`** (17,763 rows) — every live GTA 6 stream in every snapshot, across
4,141 distinct channels and 51 languages. Concurrent viewers, rank within the hour, stream title,
language, mature flag, broadcast start time, and a stable `livestream_id` so one broadcast can be
followed hour by hour.

**`kick_categories_hourly.csv`** (715 rows) — every ranked category in every snapshot, 89 distinct
categories. The context that makes the GTA 6 number mean something: what it displaced, and by how
much.

Every row carries the `apify_dataset_id` of the run that produced it, so any figure can be traced
back to its source.

## Things to try with it

- Plot the launch curve and mark the hour GTA 6 passed Just Chatting.
- Rank languages and regions by viewer-hours — the result is not the one most coverage assumes.
- Follow a single `livestream_id` across snapshots to get one streamer's audience over the night.
- Measure the long tail: how much of the 1.35M sat with the top 10 channels versus the other 889.
- Test whether GTA V lost viewers to GTA 6 or gained from the same wave of attention.
- Use the 0–4% gap between summed streams and the category total as a worked example of
  reconciling two measurements of the same quantity.

## How it was collected

Every row came from Kick.com's own public endpoints, gathered by the
[**Kick Scraper**](https://apify.com/bhole_krishna/kick-scraper) on Apify running on an hourly
schedule. No login, no private API, nothing behind a paywall.

The data stops at 19 November 05:30 UTC. Because Kick keeps no history, the only way to get the
hours after that is to collect them as they happen. The actor that produced every column here is
public, and the input behind the streamer-level file was simply:

```json
{
  "categories": ["grand-theft-auto-vi"],
  "scrapeLiveStreams": true,
  "maxItems": 1000
}
```

Put that on an hourly schedule and you are building the same record for whatever launches next.
Full column documentation and a reproducible chart script:
[github.com/krishnadubey965/gta6-kick-dataset](https://github.com/krishnadubey965/gta6-kick-dataset)

## Honest notes on the data

**Snapshots are instants, not averages.** Each row is one reading of a live counter. A peak that
fell between two snapshots is not in this data.

**The hourly series starts at 08:30 UTC.** The headline file also holds a 07:48 reading from the
run that set the schedule up. Charts here use only the 22 on-the-hour snapshots so the spacing is
even; the extra row is kept rather than deleted to tidy the series.

**Stream rows are deduplicated by channel.** Kick's paginated stream listing can return the same
channel on more than one page while the list reorders underneath the reader. Where that happened,
the highest viewer count for that channel in that snapshot was kept. The effect was small in
steady state (2–8 rows an hour) and large during the launch surge (205 of 919 rows at 10:30) —
exactly when the listing was churning fastest.

**Summed streams land 0–4% under the category total.** Adding up every stream in an hour gives
slightly less than that hour's category figure, because the two numbers are read seconds apart and
the stream listing does not reach the smallest streams in the long tail. The gap is reported
rather than smoothed; it is the honest error bar on this data, and it widens to 4.4% in the final
hour.

**`stream_started_at` is Kick's own timestamp.** It arrives without an explicit zone and is
treated as UTC.

**Language is self-declared** — the channel's setting, not detected from audio. The language
totals describe how streamers label themselves.

## Licence

CC BY 4.0. Use it commercially, publish from it, build on it; just credit the source.

> GTA 6 Launch Night on Kick.com — Hourly Viewership (2026). Collected from Kick.com with the
> Kick Scraper on Apify. https://apify.com/bhole_krishna/kick-scraper

Not affiliated with, authorised by or endorsed by Kick.com, Rockstar Games or Take-Two
Interactive.
