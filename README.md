# WQET Grading Client

## Installation

```
pip install wqet-grading
```

## Usage

```python

import wqet_grading

submission = "My Answer"
wqet_grading.grade('Sample Assessment', 'Question 1', submission)

```

## Configuration

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
