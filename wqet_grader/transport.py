#
# Note: Most of this will be server-side
#

import json
import sys
import os
import tempfile
import base64
import pandas as pd
from category_encoders import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import joblib
import requests
from urllib import error

GRADING_API_URL = os.getenv('GRADING_API_URL', 'http://localhost:2400')
VM_TOKEN = os.getenv('VM_TOKEN', '')
FAIL_ON_FIRST = os.getenv("FAIL_ON_FIRST", None)

def encode_value(value, value_type=None):
    if not value_type:
        value_type = type(value).__name__
    if value_type in ["list", "dict", "int", "float", "str"]:
        return {"type": value_type, "data": json.dumps(value)}
    if value_type in ["pandas_dataframe", "DataFrame"]:
        file = tempfile.NamedTemporaryFile()
        value.to_pickle(file.name, compression=None)
        return {
            "type": "pandas_dataframe",
            "format": "pickle",
            "data": base64.b64encode(file.read()).decode(),
        }
    if value_type in ["pandas_series", "Series"]:
        file = tempfile.NamedTemporaryFile()
        value.to_pickle(file.name, compression=None)
        return {
            "type": "pandas_series",
            "format": "pickle",
            "data": base64.b64encode(file.read()).decode(),
        }
    if value_type == "sklearn_model" or isinstance(value, (BaseEstimator, Pipeline)):
        file = tempfile.NamedTemporaryFile()
        joblib.dump(value, file.name)
        return {
            "type": "sklearn_model",
            "format": "pickle",
            "data": base64.b64encode(file.read()).decode(),
        }
    if value_type in ["file", "BufferedReader"]:
        return {"type": "file", "format": "binary", "data": base64.b64encode(value.read()).decode()}
    raise Exception("Unsupported type for encoding: {}".format(value_type))

def decode_value(value):
    value_type = value["type"]
    if value_type in ["list", "dict", "int", "float", "str"]:
        return json.loads(value["data"])
    if value_type == "pandas_dataframe":
        file = tempfile.NamedTemporaryFile()
        file.write(base64.b64decode(value["data"]))
        file.seek(0)
        return pd.read_pickle(file.name, compression=None)
    if value_type == "pandas_series":
        file = tempfile.NamedTemporaryFile()
        file.write(base64.b64decode(value["data"]))
        file.seek(0)
        return pd.read_pickle(file.name, compression=None)
    if value_type == "sklearn_model":
        file = tempfile.NamedTemporaryFile()
        file.write(base64.b64decode(value["data"]))
        file.seek(0)
        return joblib.load(file.name)
    if value_type == "file":
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(base64.b64decode(value["data"]))
        file.seek(0)
        return file
    raise Exception("Unsupported type for encoding: {}".format(value_type))

def encode_submission(object):
  encoded_submission = {
    'type': object['type']
  }
  if object['type'] == 'object':
    encoded_submission['object'] = {}
    for key,value in object['object'].items():
      encoded_submission['object'][key] = encode_value(value)
  if object['type'] == 'simple':
    encoded_submission['argument'] = []
    for value in object['argument']:
      encoded_submission['argument'].append(encode_value(value))
  return encoded_submission

def decode_submission(object):
  decoded_submission = {
    'type': object['type']
  }
  if object['type'] == 'object':
    decoded_submission['object'] = {}
    for key,value in object['object'].items():
      decoded_submission['object'][key] = decode_value(value)
  if object['type'] == 'simple':
    decoded_submission['argument'] = []
    for value in object['argument']:
      decoded_submission['argument'].append(decode_value(value))
  return decoded_submission

def remote_request(method, path, data = {}):
  headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Grader Client'
  }
  data['vmToken'] = VM_TOKEN
  try:
    r = requests.request(method, GRADING_API_URL + path, headers=headers, json=data)
    content = r.text
    return json.loads(content)
  except error.HTTPError as e:
    raise Exception('Could not connect to Grading Service API: {}'.format(str(e)))
  except Exception as e:
    raise Exception('Could not connect to Grading Service API: {}'.format(str(e)))

def grade_submission(assessment_id, question_id, submission_object):
  result = None
  encoded_submission_object = None
  try:
    encoded_submission_object = encode_submission(submission_object)
  except Exception as e:
    raise Exception('Could not encode this submission for remote grading: {}'.format(str(e)))
  data = {
    'assessment': assessment_id,
    'question': question_id,
    'submission': encoded_submission_object
  }
  envelope = remote_request('POST', '/1/grade', data)
  error = envelope.get('error', None)
  if error != None:
    if error.get('raisedByGrader', False) == True:
      raise Exception('Grader raised error: {}'.format(error['message']))
    else:
      raise Exception('Could not grade submission: {}'.format(error['message']))
  result = envelope['data']['result']
  
  # Used only in testing
  if FAIL_ON_FIRST and not result["passed"]:
    raise Exception(
      f"Testing Error. Submission for assessment `{assessment_id} - {question_id}` failed."
    )
  return result

