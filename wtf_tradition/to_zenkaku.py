"""
$ python to_zenkaku.py spam42ﾊﾑ
ｓｐａｍ４２ハム
"""

import argparse

import jaconv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hankaku")
    args = parser.parse_args()

    zenkaku = jaconv.h2z(args.hankaku, kana=True, ascii=True, digit=True)
    print(zenkaku)
