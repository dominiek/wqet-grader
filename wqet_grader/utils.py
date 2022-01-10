import os

grading_content_path = os.getenv("GRADING_CONTENT_PATH", None)

def set_grading_content_path(path):
    global grading_content_path
    grading_content_path = path

def get_grading_content_path():
    if not grading_content_path:
        raise Exception("No grading content path was set")
    return grading_content_path
