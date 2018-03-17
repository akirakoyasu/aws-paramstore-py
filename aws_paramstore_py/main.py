import boto3


def get(*paths, decryption=False, ssm_client=None):
    if ssm_client is None:
        ssm_client = boto3.client('ssm')
    path = _join_slashes(paths)
    yields = _yield_parameters(ssm_client, Path=path, Recursive=True, WithDecryption=decryption)
    params = (_remove_prefix(p, path) for p in yields)
    return _convert_to_dict(params)


def _join_slashes(paths):
    path = '/'.join(_remove_slashes_on_edge(e) for e in paths)
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


def _yield_parameters(ssm_client, *args, **kwargs):
    response = ssm_client.get_parameters_by_path(*args, **kwargs)
    for parameter in response['Parameters']:
        yield parameter
    while 'NextToken' in response:
        next_token = response['NextToken']
        response = ssm_client.get_parameters_by_path(*args, NextToken=next_token, **kwargs)
        for parameter in response['Parameters']:
            yield parameter


def _remove_prefix(param, prefix):
    name = param['Name']
    if _is_led_by_slash(name):
        name = param['Name'][len(prefix):]
    param['Name'] = name
    return param


def _convert_to_dict(params):
    return {p['Name']: p['Value'] for p in params}
