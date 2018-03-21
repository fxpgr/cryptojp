
test:
	python -m unittest discover tests

rst:
	pandoc README.md --toc -o README.rst

docs:
	cd docs && make html
