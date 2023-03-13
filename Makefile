init:
	pip install -r requirements.txt

test:
	py.test tests

down:
	pip uninstall -r requirements.txt
