.PHONY: all test

all: test

test:

clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm {} \;
	@find . -name '__pycache__' -type d | xargs rm -rf

make-docs:
	$(MAKE) -C docs html

install:
	@pip install --editable .

.PHONY: clean clean-pyc install make-docs
