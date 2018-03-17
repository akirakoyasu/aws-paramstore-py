import argparse
import json
import shlex

from .main import get

__version__ = '0.1.0'


def cli():
    def print_bash_export(params):
        for key, value in params.items():
            var_name = key.replace('/', '_').replace('-', '_').replace('.', '_')
            var_val = shlex.quote(value)
            print('export {0}={1}'.format(var_name, var_val))

    parser = argparse.ArgumentParser(description='Query params from AWS System Manager Parameter Store')
    parser.add_argument('paths', metavar='path', nargs='*', help='The hierarchy for the parameters')
    parser.add_argument('--decryption', action='store_true', help='Decrypt secure values or not')
    parser.add_argument('--bash-export', action='store_true', help='Print bash export script')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()

    params = get(*args.paths, decryption=args.decryption)
    if args.bash_export:
        print_bash_export(params)
    else:
        print(json.dumps(params))
