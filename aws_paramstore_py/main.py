import boto3


def get(*paths, decryption=False):
    ssm = boto3.client('ssm')
    path = _join_slashes(paths)
    response = ssm.get_parameters_by_path(Path=path, Recursive=True, WithDecryption=decryption)
    params = map(lambda p: _remove_prefix(p, path), response['Parameters'])
    return _convert_to_dict(params)


def _join_slashes(paths):
    path = '/'.join(filter(lambda e: len(e), map(lambda e: _remove_slashes_on_edge(e), paths)))
    if not path:
        return '/'
    else:
        return '/' + path + '/'


def _remove_slashes_on_edge(string):
    if _is_led_by_slash(string):
        string = string[1:]
    if _is_followed_by_slash(string):
        string = string[:-1]
    return string


def _is_led_by_slash(string):
    return string[:1] == '/'


def _is_followed_by_slash(string):
    return string[-1:] == '/'


def _remove_prefix(param, prefix):
    param['Name'] = param['Name'][len(prefix):]
    return param


def _convert_to_dict(params):
    return {p['Name']: p['Value'] for p in params}
