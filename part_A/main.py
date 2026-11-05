import json

import pandas as pd

from parse import ArticleProcessor

INPUT_JSON_PATH = "input.json"


def main():
    with open(INPUT_JSON_PATH) as f:
        articles_df = pd.DataFrame(json.load(f))

    counts = ArticleProcessor().run(articles_df)
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()