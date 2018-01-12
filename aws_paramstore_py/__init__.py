import argparse
import json

import boto3

__version__ = '0.0.1'


def main():
    parser = argparse.ArgumentParser(description='Query values from AWS System Manager Parameter Store')
    parser.add_argument('paths', metavar='path', nargs='*', help='The hierarchy for the parameter')
    parser.add_argument('--decryption', action='store_true', help='Decrypt secure values or not')
    args = parser.parse_args()
    paths = args.paths
    decryption = args.decryption
    params = get(*paths, decryption=decryption)
    print(json.dumps(params))


def get(*paths, decryption=False):
    ssm = boto3.client('ssm')
    path = '/'.join(paths)
    if path[:1] != '/':
        path = '/' + path
    if path[len(path):] != '/':
        path = path + '/'
    response = ssm.get_parameters_by_path(Path=path, Recursive=True, WithDecryption=decryption)
    params = map(lambda p: _remove_prefix(p, path), response['Parameters'])
    return _convert_to_map(params)


def _remove_prefix(param, prefix):
    param['Name'] = param['Name'][len(prefix):]
    return param


def _convert_to_map(params):
    return {p['Name']: p['Value'] for p in params}
