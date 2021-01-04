"""Totaling the impressive talks from the participant questionnaires."""

import argparse
import csv
from collections import Counter

best_talk_column_header = (
    "Q13. 印象に残った講演を選んでください/"
    "Which presentations you were most impressed by (multiple choice)?"
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    args = parser.parse_args()

    with open(args.input_csv) as fin:
        reader = csv.reader(fin)
        header = next(reader)
        best_talk_index = header.index(best_talk_column_header)
        best_talk_answers = [row[best_talk_index] for row in reader]

    print(len(best_talk_answers))
    assert len(best_talk_answers) == 120

    flatten = []
    for answer in best_talk_answers:
        if not answer:  # 回答なしを除く
            continue
        if ", " not in answer:  # 複数選択の区切り文字を含まない
            flatten.append(answer)
        else:
            multiple_choice = answer.split(", ")
            flatten.extend(multiple_choice)
    print(len(flatten))

    counter = Counter(flatten)
    print(len(counter))

    with open(args.output_csv, "w") as fout:
        writer = csv.writer(fout)
        writer.writerows(counter.most_common())
