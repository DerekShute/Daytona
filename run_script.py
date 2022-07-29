#!/bin/python3
'''
Run some script.
'''

from os.path import exists
import sys
import argparse
import yaml
import daytona


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run Daytona script')
    parser.add_argument('script', type=str,
                        help='script file name')
    parser.add_argument('--main', default='main', type=str,
                        help='script start keyword')
    args = parser.parse_args()

    if not exists(args.script):
        print(f'No such file {args.script}')
        sys.exit(1)

    with open(args.script, 'r') as f:
        body_dict = yaml.safe_load(f)

    daytona.register_keywords(body_dict)
    daytona.execute_script(args.main)

# EOF
