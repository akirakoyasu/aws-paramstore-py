import argparse
import json

from .main import get

__version__ = '0.0.4'


def cli():
    parser = argparse.ArgumentParser(description='Query params from AWS System Manager Parameter Store')
    parser.add_argument('paths', metavar='path', nargs='*', help='The hierarchy for the parameter')
    parser.add_argument('--decryption', action='store_true', help='Decrypt secure values or not')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    paths = args.paths
    decryption = args.decryption
    params = get(*paths, decryption=decryption)
    print(json.dumps(params))
