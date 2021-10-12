# WQET Grader Client

## Installation

```
pip install wqet-grader
```

## Usage

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

## Configuration

Through environment variables:

- `GRADING_API_URL` - URL of grading API
- `VM_TOKEN` - Temporary token for user authentication

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
