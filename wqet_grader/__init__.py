
import os
import sys
from .transport import grade_submission, remote_request

def grade(assessment_id, question_id, submission):
  submission_object = {
    'type': 'simple',
    'argument': [submission]
  }
  return grade_submission(assessment_id, question_id, submission_object)

def grade_object(assessment_id, question_id, **kwargs):
  submission_object = {
    'type': 'object',
    'object': kwargs
  }
  return grade_submission(assessment_id, question_id, submission_object)

def get_system_info():
  return {
    'hostname': os.popen('hostname').read().strip(),
    'platform': sys.platform.lower(),
    'uptime': os.popen('uptime').read().strip(),
  }

def init(assessment_id):
  data = {
    'assessment': assessment_id,
    'event_type': 'loaded',
    'event': {
      'info': get_system_info()
    },
  }
  remote_request('POST', '/1/track', data)