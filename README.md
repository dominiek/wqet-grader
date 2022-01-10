# WQET Grader Client

## Installation

```
pip install wqet-grader
```

## Usage: Notebooks

Simple grading:

```python

import wqet_grader

submission = "My Answer"
wqet_grader.grade('Sample Assessment', 'Question 1', submission)

```

Object grading:

```python

import wqet_grader

arg1 = 3.14
arg2 = "something else"
wqet_grader.grade_object('Sample Assessment', 'Question 1', arg1=arg1, arg2=arg2)

```

Supported objects:

- `file` Binary file
- `pandas_dataframe` Pandas DataFrame object
- `sklearn_model` SKLearn pipeline/model
- `float`, `int`, `string`, `dict`, `list` - Primative types

## Usage: Content Development Debugging

You can load a directory of grading algorithm modules, by running the following command:

```bash
./scripts/load_and_run fixtures/content
```

This will automatically restart the server when any changes to the Grading API code or content is detected. Reporting to the WQET platform is disabled and additional debug logging is enabled on the console.

The sample notebook of this content can be run as follows:

```bash
cd fixtures/notebooks
./run.sh
```

Then open: http://127.0.0.1:8888/lab/tree/sample-questions.ipynb?token=test

## Usage: Content Integration Testing

You can spin up a grading server for a directory of content, using the following code:

```python
from wqet_grader.utils import set_grading_content_path
set_grading_content_path("my-curriculum-folder")

from wqet_grader.server import app
app.run(host="localhost", port=2400, debug=True, threaded=False)
```

## Configuration

Through environment variables:

- `GRADING_API_URL` - URL of grading API
- `VM_TOKEN` - Temporary token for user authentication
- `SCORE_OUTPUT_FORMAT` - Format of score output in notebook: `json` or `html` (defaults to JSON)

## Development Setup

Requirements:

- Python 3.6+.

Setup your Virtual Environment:

```bash
make venv
```

## Testing

To run unit tests:

```bash
make test
```

## Packaging

```bash
make package.build
make package.release
```
