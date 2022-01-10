import importlib
import json
import logging
import os

my_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class GraderException(Exception):
    def __init__(self, message, original_error, function):
        self.message = message
        self.original_error = original_error
        self.function = function
        super().__init__(self.message)


def load_assessment_definitions(dir_path):
    objects = []
    paths = os.listdir(dir_path)
    for path in paths:
        full_path = os.path.join(dir_path, path)
        if os.path.isdir(full_path):
            logging.info("Loading assessment definitions for: {}".format(full_path))
            index_file = full_path + "/index.json"
            if not os.path.isfile(index_file):
                raise Exception("Expected file: {}".format(index_file))
            with open(index_file, "r") as f:
                try:
                    object = json.load(f)
                    object["path"] = full_path
                    objects.append(object)
                except Exception as e:
                    raise Exception("Could not parse JSON file {} ({})", index_file, str(e))
    return objects


def get_assessment_definition(assessment_definitions, assessment_id):
    for assessment_definition in assessment_definitions:
        if assessment_definition["id"] == assessment_id:
            return assessment_definition
    return None


def get_grader_definition(assessment_definitions, assessment_id, question_id):
    assessment_definition = get_assessment_definition(assessment_definitions, assessment_id)
    if not assessment_definition:
        raise Exception("Could not find assessment definition with id {}".format(assessment_id))
    graders = assessment_definition.get("graders", [])
    for grader in graders:
        if grader["id"] == question_id:
            return assessment_definition, grader
    return assessment_definition, None


def load_grading_module(assessment_definition):
    python_dir = assessment_definition["path"] + "/python/"
    code_path = python_dir + "grading.py"
    logging.info("Loading Python code module: {}".format(code_path))
    spec = importlib.util.spec_from_file_location(
        "grading_module", code_path, submodule_search_locations=python_dir
    )
    grading_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grading_module)
    return grading_module


def execute_grading(assessment_definitions, assessment_id, question_id, submission_object):
    assessment_definition, grader_definition = get_grader_definition(
        assessment_definitions, assessment_id, question_id
    )
    if not grader_definition:
        raise Exception(
            "Could not find grader definition with id {}/{}".format(assessment_id, question_id)
        )
    grading_module = load_grading_module(assessment_definition)
    logging.info("Executing Python grading function: {}".format(grader_definition["function"]))
    fn = getattr(grading_module, grader_definition["function"])
    if not fn:
        raise Exception(
            "Could not detmine grading function for question {}/{}".format(
                assessment_id, question_id
            )
        )
    defaults = grader_definition.get("defaults", {})
    result = None
    try:
        if submission_object["type"] == "object":
            result = fn(defaults, **submission_object["object"])
        else:
            result = fn(defaults, submission_object["argument"][0])
        # Ensure no funny _bool objects are there:
        if "passed" in result:
            result["passed"] = bool(result["passed"])
        result["numGraders"] = len(assessment_definition["graders"])
        return result
    except Exception as e:
        raise GraderException(str(e), e, grader_definition["function"])
