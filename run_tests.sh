#!/bin/bash
pytest .
mypy .
pylint zxtransformer/ test/
