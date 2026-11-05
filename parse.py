from datetime import datetime

import pandas as pd


class ArticleProcessor:
    DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y")

    def normalize_text(self, df):
        df = df.copy()
        df["title"] = df["title"].str.strip().str.replace(r"\s+", " ", regex=True)
        df["topic"] = df["topic"].str.strip().str.lower()
        return df

    def normalize_dates(self, df):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"].map(self._parse_date))
        return df

    def _parse_date(self, value):
        value = value.strip()
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {value!r}")

    def deduplicate(self, df):
        # Titles are compared case-insensitively; the first occurrence is kept.
        is_dup = df["title"].str.casefold().duplicated(keep="first")
        return df[~is_dup].reset_index(drop=True)

    def weekly_counts(self, df):
        # Calendar week = ISO week (Monday to Sunday). The ISO year is used so
        # that dates near New Year land in the correct week.
        iso = df["date"].dt.isocalendar()
        week = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
        return (
            df.assign(week=week)
            .groupby(["week", "topic"])
            .size()
            .reset_index(name="count")
            .sort_values(["week", "topic"], ignore_index=True)
        )

    def run(self, df):
        df = self.normalize_text(df)
        df = self.normalize_dates(df)
        df = self.deduplicate(df)
        return self.weekly_counts(df)
