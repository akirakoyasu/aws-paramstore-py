# aws-paramstore-py

Query params from AWS System Manager Parameter Store

## Install

```bash
pip install aws-paramstore-py
```

## Usage

in console
```bash
# AWS credentials from env vars
aws-pspy /path/to/params
# returns {"key1": "value1", "key2": "value2"}
```

in Python
```python
import aws_paramstore_py as paramstore

# AWS credentials from env vars
params = paramstore.get('/path/to/params')
# dict(key1: "value1", key2: "value2")
```
