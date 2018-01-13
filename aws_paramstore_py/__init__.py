import argparse
import json

import boto3

__version__ = '0.0.3'


def main():
    parser = argparse.ArgumentParser(description='Query params from AWS System Manager Parameter Store')
    parser.add_argument('paths', metavar='path', nargs='*', help='The hierarchy for the parameter')
    parser.add_argument('--decryption', action='store_true', help='Decrypt secure values or not')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    paths = args.paths
    decryption = args.decryption
    params = get(*paths, decryption=decryption)
    print(json.dumps(params))


def get(*paths, decryption=False):
    ssm = boto3.client('ssm')
    path = '/'.join(paths)
    path = _complement_slashes(path)
    response = ssm.get_parameters_by_path(Path=path, Recursive=True, WithDecryption=decryption)
    params = map(lambda p: _remove_prefix(p, path), response['Parameters'])
    return _convert_to_dict(params)


def _complement_slashes(path):
    if path[len(path):] != '/':
        path = path + '/'
    if path[:1] != '/':
        path = '/' + path
    return path


def _remove_prefix(param, prefix):
    param['Name'] = param['Name'][len(prefix):]
    return param


def _convert_to_dict(params):
    return {p['Name']: p['Value'] for p in params}
