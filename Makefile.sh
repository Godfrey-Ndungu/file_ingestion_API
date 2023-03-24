#!/bin/bash

# Activate the virtual environment
source venv/bin/activate
cd fileUpload

# Run Flake8 to check for PEP8 violations
flake8 --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=migrations .
flake8_status=$?

# Run Black to check and format the code
black . --check --diff
black_status=$?

# If either Flake8 or Black has issues, display a helpful message
if [ $flake8_status != 0 ] || [ $black_status != 0 ]; then
  echo ""
  echo "COMMIT REJECTED: Please fix the following issues before committing:"
  echo ""
  if [ $flake8_status != 0 ]; then
    echo "* PEP8 style guide violations detected in the following files:"
    echo ""
    flake8 --select=E9,F63,F7,F82 --show-source --exclude=migrations .
    echo ""
  fi
  if [ $black_status != 0 ]; then
    echo "* Code formatting issues detected in the following files:"
    echo ""
    black --diff .
    echo ""
  fi
  echo "Aborting commit."
  exit 1
fi

# Deactivate the virtual environment
deactivate

exit 0