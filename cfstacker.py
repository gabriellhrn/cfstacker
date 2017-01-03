
import sys
import argparse

PROG = sys.argv[0]
VERSION = 0.1

# functions
def parse_args():
    parser = argparse.ArgumentParser(prog=PROG,
            description='Manages CloudFormation template files (YAML or JSON) stored at "templates/"')

    return parser.parse_args()

# main
def main():
    args = parse_args()

if __name__ == "__main__":
    main()

