"""CLI tool which converts credentials JSON file to oneliner 
to use Lambda Environment Variable instead of AWS Secrets Manager.

Copy the oneline and paste in Lambda Environment Variable.
"""

import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dest")
    args = parser.parse_args()

    with open(args.src) as f_src, open(args.dest, "w") as f_dest:
        credentials = json.load(f_src)
        json.dump(credentials, f_dest)
