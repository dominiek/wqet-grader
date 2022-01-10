import json
import logging
import os

from flask import Blueprint, abort, g, jsonify, request

from ..grading import GraderException, execute_grading, load_assessment_definitions
from ..transport import decode_submission, encode_value
from ..utils import get_grading_content_path

CONTENT_MODE = os.getenv("CONTENT_MODE", None)

app = Blueprint("grade", __name__)
definitions = load_assessment_definitions(get_grading_content_path())

@app.route("/grade", methods=["POST"])
def grade():
    envelope = request.json
    assessment_id = envelope.get("assessment", None)
    if assessment_id == None:
        abort(400, "Need assessment")
    question_id = envelope.get("question", None)
    if question_id == None:
        abort(400, "Need question")
    
    raw_submission = envelope.get("submission", {})
    decoded_submission = decode_submission(raw_submission)
    try:
        logging.info("Executing grading for {} / {}".format(assessment_id, question_id))
        result = execute_grading(definitions, assessment_id, question_id, decoded_submission)
        logging.info(
            "Result for {} / {}: {}".format(assessment_id, question_id, json.dumps(result))
        )
    except GraderException as error:
        logging.warn(
            "Error came back from grader for {} / {}: {} (function={})".format(
                assessment_id, question_id, str(error), error.function
            )
        )
        return jsonify({"error": {"code": 500, "raisedByGrader": True, "message": str(error)}})
    
    result_envelope = {"score": result["score"], "passed": result.get("passed", False)}
    if result.get('comment', None) != None:
        result_envelope['comment'] = result['comment']
    image_path = result.get('image', None)
    if image_path != None:
      try:
        with open(image_path, 'rb') as f:
          result_envelope['image'] = encode_value(f, 'file')
      except Exception as error:
        return jsonify(
            {
                "error": {
                    "code": 500,
                    "message": "Could not serialize result image: {}".format(
                        str(error)
                    ),
                }
            }
        )
    return jsonify(
        {"data": {"result": result_envelope}}
    )
