# https://gist.github.com/ftnext/2e14fb57c96ca276ee4d28eccfcecd96

import argparse

from janome.analyzer import Analyzer
from janome.tokenfilter import (
    POSKeepFilter,
    POSStopFilter,
    ExtractAttributeFilter,
)
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_text")
    parser.add_argument("output_image")
    parser.add_argument("--font_path", default="ipagp.ttf")
    parser.add_argument("--random_state", type=int, default=1)
    parser.add_argument("--max_words", type=int, default=30)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=674)
    args = parser.parse_args()

    t = Tokenizer()
    token_filters = [
        POSKeepFilter(["名詞"]),  # "動詞"
        POSStopFilter(["名詞,非自立", "名詞,代名詞", "動詞,非自立"]),
        ExtractAttributeFilter("base_form"),
    ]
    a = Analyzer(tokenizer=t, token_filters=token_filters)

    with open(args.input_text, encoding="utf-8") as f:
        text = f.read()
        tokens = a.analyze(text)

    wordcloud = WordCloud(
        font_path=args.font_path,
        background_color="white",
        width=args.width,
        height=args.height,
        collocations=False,
        random_state=args.random_state,
        max_words=args.max_words,
    ).generate(" ".join(tokens))
    wordcloud.to_image().save(args.output_image)
