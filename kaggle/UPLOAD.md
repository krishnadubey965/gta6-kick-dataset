# Publishing this to Kaggle

Two ways. The web form is fine; the CLI is faster if you will update the dataset later.

## Option A — the website

1. Go to <https://www.kaggle.com/datasets> and click **New Dataset**.
2. Upload the three files from `../data/`:
   - `gta6_viewers_hourly.csv`
   - `gta6_streams_hourly.csv`
   - `kick_categories_hourly.csv`
3. Title: **GTA 6 Launch Night on Kick.com: Hourly Viewers**
4. Subtitle: **22 hourly snapshots: 7,905 to 1,353,198 concurrent viewers in 15 hours**
5. Paste the whole of `description.md` into the description field — it renders as Markdown.
6. Licence: **CC BY 4.0**.
7. Tags: `internet`, `video games`, `social networks`, `time series`.
8. Set a cover image: `../chart-light.svg` exported to PNG, or a screenshot of it.
9. Publish, then paste the GitHub repo link in the first comment.

## Option B — the Kaggle CLI

```bash
pip install kaggle
# put your API token at ~/.kaggle/kaggle.json first (Kaggle > Settings > Create New Token)

cd kaggle
# 1. Replace YOUR_KAGGLE_USERNAME in dataset-metadata.json with your Kaggle username.
# 2. Stage the three CSVs beside the metadata file, which is where the CLI expects them:
cp ../data/*.csv .
kaggle datasets create -p . --dir-mode zip
```

To push an updated version later, after collecting more hours:

```bash
cp ../data/*.csv .
kaggle datasets version -p . -m "Adds snapshots through <date>"
```

## After publishing

The description already links to the actor and the GitHub repo, which is the point of
publishing here. Two things worth doing on the day:

- **Add a starter notebook.** A dataset with a notebook attached gets recommended far more
  often than a bare dataset. Ten lines that load `gta6_viewers_hourly.csv` and plot the curve
  is enough.
- **Keep the title's search terms.** "GTA 6", "Kick" and "viewers" are what people will type.
