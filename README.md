# aws-paramstore-py

[![Build Status](https://travis-ci.org/akirakoyasu/aws-paramstore-py.svg?branch=master)](https://travis-ci.org/akirakoyasu/aws-paramstore-py)

Query params from AWS System Manager Parameter Store

## Install

```bash
pip install aws-paramstore-py
```

## Usage

in shell
```bash
# AWS credentials from env vars
aws-pspy /path/to/params
# returns {"key1": "value1", "key2": "value2"}

eval "$(aws-pspy /path/to/params --bash-export)"
# set env vars:
# - key1="value1"
# - key2="value2"
```

in Python
```python
import aws_paramstore_py as paramstore

# use default boto3 ssm client
params = paramstore.get('/path/to/params')
# dict(key1: "value1", key2: "value2")

# use your own boto3 ssm client
import boto3
ssm = boto3.client('ssm')
params = paramstore.get('/path/to/params', ssm_client=ssm)
```
