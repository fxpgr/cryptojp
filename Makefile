
test:
	python -m unittest discover tests

rst:
	pandoc README.md -o README.rst
