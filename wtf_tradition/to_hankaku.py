import argparse
import unicodedata
# TODO: normalizeなので半角カナが残らない

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zenkaku")
    args = parser.parse_args()

    hankaku = unicodedata.normalize("NFKD", args.zenkaku)
    print(hankaku)
