import unittest
from unittest.mock import patch

import aws_paramstore_py as paramstore


@patch('aws_paramstore_py.main.boto3')
class TestMain(unittest.TestCase):
    def test_get(self, mock):
        method = mock.client('ssm').get_parameters_by_path
        method.return_value = {'Parameters': [
            {'Name': '/path/to/params/key1', 'Value': "value1"},
            {'Name': '/path/to/params/key2', 'Value': "value2"}
        ]}

        params = paramstore.get('path', 'to', 'params')

        method.assert_called_with(Path='/path/to/params/', Recursive=True, WithDecryption=False)
        self.assertDictEqual({"key1": "value1", "key2": "value2"}, params)

    def test_get_root(self, mock):
        method = mock.client('ssm').get_parameters_by_path

        paramstore.get()

        method.assert_called_with(Path='/', Recursive=True, WithDecryption=False)

    def test_get_slash(self, mock):
        method = mock.client('ssm').get_parameters_by_path
        method.return_value = {'Parameters': [
            {'Name': '/path/to/params/key1', 'Value': "value1"},
            {'Name': '/path/to/params/key2', 'Value': "value2"},
            {'Name': 'root-key3', 'Value': "value3"}
        ]}

        params = paramstore.get('/')

        method.assert_called_with(Path='/', Recursive=True, WithDecryption=False)
        self.assertDictEqual({
            "path/to/params/key1": "value1",
            "path/to/params/key2": "value2",
            "root-key3": "value3"
        }, params)

    def test_get_leading_slash(self, mock):
        method = mock.client('ssm').get_parameters_by_path

        paramstore.get('/path/to')

        method.assert_called_with(Path='/path/to/', Recursive=True, WithDecryption=False)

    def test_get_following_slash(self, mock):
        method = mock.client('ssm').get_parameters_by_path

        paramstore.get('path/to/')

        method.assert_called_with(Path='/path/to/', Recursive=True, WithDecryption=False)

    def test_get_with_decryption(self, mock):
        method = mock.client('ssm').get_parameters_by_path

        paramstore.get('path/to/params', decryption=True)

        method.assert_called_with(Path='/path/to/params/', Recursive=True, WithDecryption=True)
