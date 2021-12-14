
import os
import sys
from .transport import decode_value, grade_submission, remote_request
import importlib

has_ipython = False
if importlib.util.find_spec("IPython") is not None:
  has_ipython = True
  from IPython.core.display import display, HTML
  from PIL import Image as PilImage

SCORE_OUTPUT_FORMAT = os.getenv('SCORE_OUTPUT_FORMAT', 'json')

if has_ipython == False:
  SCORE_OUTPUT_FORMAT = 'json'

def init_html():
  html = '''
<style>
  
  .checkmark {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #fff;
    stroke-miterlimit: 10;
    box-shadow: inset 0px 0px 0px #7ac142;
    animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
  }
  
  .checkmark__circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 2;
    stroke-miterlimit: 10;
    stroke: #7ac142;
    fill: none;
    animation: stroke .6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;
  }
  
  .checkmark__check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke .3s cubic-bezier(0.650, 0.000, 0.450, 1.000) .8s forwards;
  }
  
  .failmark {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #fff;
    stroke-miterlimit: 10;
    box-shadow: inset 0px 0px 0px #F34811;
    animation: failfill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
  }
  
  .failmark__circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 2;
    stroke-miterlimit: 10;
    stroke: #F34811;
    fill: none;
    animation: stroke .6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;
  }
  
  @keyframes stroke {
    100% {
      stroke-dashoffset: 0;
    }
  }
  
  @keyframes scale {
    0%, 100% {
      transform: none;
    }
    50% {
      transform: scale3d(1.1, 1.1, 1);
    }
  }
  
  @keyframes fill {
    100% {
      box-shadow: inset 0px 0px 0px 30px #7ac142;
    }
  }
  
  @keyframes failfill {
    100% {
      box-shadow: inset 0px 0px 0px 30px #F34811;
    }
  }
  
  
  .wqet-result {
    width: 450px;
    clear: both;
  }
  
  .wqet-result .animation {
    float: left;
    width: 100px;
  }
  
  .wqet-result .animation .checkmark,
  .wqet-result .animation .failmark {
    margin: 20px auto 20px auto;
  }
  
  .wqet-result .details {
    float: right;
    width: 349px;
    padding: 28px 0;
  }
  
  .wqet-result .details .title {
    font-weight: bold;
    font-size: 110%;
  }
  .wqet-result .details p {
    margin: 0;
  }
</style>
'''
  display(HTML(html))

def render_score_html(result):
  comment = result.get('comment', 'Please Try Again :(')
  html = '''
  <div class="wqet-result">
    <div class="animation">
      <svg class="failmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
        <circle class="failmark__circle" cx="26" cy="26" r="25" fill="none"/>
      </svg>
    </div>
    <div class="details">
      <p class="title">$comment</p>
      <p>Score: $score</p>
    </div>
  </div>
'''
  if result.get('passed', False) == True:
    comment = result.get('comment', 'Question Passed!')
    html = '''
    <div class="wqet-result">
      <div class="animation">
        <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
          <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
          <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
        </svg>
      </div>
      <div class="details">
        <p class="title">$comment</p>
        <p>Score: $score</p>
      </div>
    </div>
'''
  display(HTML(html.replace('$score', str(result['score'])).replace('$comment', comment)))
  if result.get('image', None) != None:
    image = decode_value(result['image'])
    pil_image = PilImage.open(image)
    display(pil_image)

def show_score(result):
  if SCORE_OUTPUT_FORMAT == 'json':
    return result
  render_score_html(result)

def grade(assessment_id, question_id, submission):
  submission_object = {
    'type': 'simple',
    'argument': [submission]
  }
  return show_score(grade_submission(assessment_id, question_id, submission_object))

def grade_object(assessment_id, question_id, **kwargs):
  submission_object = {
    'type': 'object',
    'object': kwargs
  }
  return show_score(grade_submission(assessment_id, question_id, submission_object))

def get_system_info():
  return {
    'hostname': os.popen('hostname').read().strip(),
    'platform': sys.platform.lower(),
    'uptime': os.popen('uptime').read().strip(),
  }

def init(assessment_id):
  if SCORE_OUTPUT_FORMAT != 'json':
    init_html()
  data = {
    'assessment': assessment_id,
    'event_type': 'loaded',
    'event': {
      'info': get_system_info()
    },
  }
  remote_request('POST', '/1/track', data)

