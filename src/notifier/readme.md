# overview

# test
. .venv/bin/activate
pip install pytest slack_sdk
cd ../src/notifier
PYTHONPATH=. pytest tests/test_main.py
