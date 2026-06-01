"""Generate word clouds from Naver Finance news titles."""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from pathlib import Path
import re

from konlpy.tag import Okt
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from .config import asset_dir
from .data_collection import crawl_naver_finance_titles


BRACKET_TEXT_PATTERN = re.compile(r"\[[^)]*\]")
DEFAULT_STOPWORDS = {
    "코스피",
    "코스닥",
    "주간",
    "증시",
    "금융",
    "뉴스",
}


def clean_title(title: str) -> str:
    """Remove bracketed press labels and normalize whitespace."""

    title = BRACKET_TEXT_PATTERN.sub("", title)
    return " ".join(title.split())


def collect_recent_titles(min_titles: int = 150) -> list[str]:
    """Collect today's titles, then add yesterday's titles if the sample is small."""

    today = date.today()
    titles = [clean_title(title) for title in crawl_naver_finance_titles()]
    if len(titles) >= min_titles:
        return titles

    yesterday = (today - timedelta(days=1)).strftime("%Y%m%d")
    titles.extend(clean_title(title) for title in crawl_naver_finance_titles(yesterday))
    return titles[:min_titles]


def extract_keyword_counts(
    titles: list[str],
    stopwords: set[str] | None = None,
) -> Counter[str]:
    """Extract Korean nouns and count keywords for a word cloud."""

    stopwords = stopwords or DEFAULT_STOPWORDS
    nouns = Okt().nouns("\n".join(titles))
    words = [noun for noun in nouns if len(noun) > 1 and noun not in stopwords]
    return Counter(words)


def generate_wordcloud(
    counts: Counter[str],
    output_path: Path | None = None,
    font_path: str = "malgun",
) -> Path:
    """Generate and save a word cloud image."""

    output_path = output_path or asset_dir() / f"news_wordcloud_{date.today():%Y-%m-%d}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        colormap="copper",
        width=800,
        height=400,
        max_font_size=120,
    ).generate_from_frequencies(counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file(str(output_path))
    plt.close()
    return output_path


def main() -> None:
    titles = collect_recent_titles()
    counts = extract_keyword_counts(titles)
    output_path = generate_wordcloud(counts)
    print(f"Saved word cloud: {output_path}")


if __name__ == "__main__":
    main()
