
import sys
import argparse

PROG = sys.argv[0]
VERSION = 0.1

# functions
def parse_args():
    parser = argparse.ArgumentParser(prog=PROG,
            description='Manages CloudFormation template files (YAML or JSON) stored at "templates/"')

    parser.add_argument('-V', '--version', action='version', version='%s version %s' % (PROG, VERSION))

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-b', '--boilerplate', action='store_true',
            help='generate boilerplate for TEMPLATE')
    group.add_argument('-c', '--create', action='store_true',
            help='create an ecs stack based on TEMPLATE')
    group.add_argument('-d', '--delete', action='store_true',
            help='delete TEMPLATE\'s stack')
    group.add_argument('-u', '--update', action='store_true',
            help='update TEMPLATE\'s stack')

    parser.add_argument('template', metavar='TEMPLATE', type=str,
            help='name of a CloudFormation file (YAML or JSON) to be managed')
    parser.add_argument('parameters', metavar='PARAMETERS', type=str, nargs='?',
            help='name of a json file containing parameters to be used in TEMPLATE (optional)')

    return parser.parse_args()

# main
def main():
    args = parse_args()

if __name__ == "__main__":
    main()

