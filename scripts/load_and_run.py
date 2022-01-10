import logging
import sys

from wqet_grader.utils import set_grading_content_path

if len(sys.argv) < 2:
    print("Usage: {} <grading_content_path>".format(sys.argv[0]))
    sys.exit(1)

set_grading_content_path(sys.argv[1])
from wqet_grader.server import app

app.logger.setLevel(logging.DEBUG)
app.run(host="localhost", port=2400, debug=True, threaded=False)
