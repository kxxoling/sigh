APP = sigh
TRANS_DIR = translations

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

# translate
babel-extract:
	pybabel extract -F $(APP)/babel.cfg -o $(APP)/$(TRANS_DIR)/messages.pot .

babel-init: babel-extract
	pybabel init -i $(APP)/$(TRANS_DIR)/messages.pot -d $(APP)/$(TRANS_DIR) -l zh_CN

babel-compile:
	pybabel compile -d $(APP)/$(TRANS_DIR)

babel-update: babel-extract
	pybabel update -i $(APP)/$(TRANS_DIR)/messages.pot -d $(APP)/$(TRANS_DIR)

.PHONY: babel-extract babel-init babel-compile babel-update
