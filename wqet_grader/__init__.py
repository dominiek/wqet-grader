
from .transport import grade_submission

def grade(assessment_id, question_id, submission):
  submission_object = {
    'type': 'simple',
    'argument': submission
  }
  return grade_submission(assessment_id, question_id, submission_object)

def grade_object(assessment_id, question_id, **kwargs):
  submission_object = {
    'type': 'object',
    'object': kwargs
  }
  return grade_submission(assessment_id, question_id, submission_object)
