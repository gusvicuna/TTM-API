init:
	pip install -r requirements.txt

test:
	python -m pytest Tests

down:
	pip uninstall -r requirements.txt
