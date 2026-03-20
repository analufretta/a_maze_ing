# TODO: revise Makefile

PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT_FILE = $(shell grep "^OUTPUT_FILE=" config.txt | cut -d'=' -f2)


help:
	@echo ""
	@echo "a-maze-ing Makefile"
	@echo "------------------"
	@echo "make install       Install project dependencies"
	@echo "make run           Run program with $(CONFIG)"
	@echo "make debug         Run program in pdb with $(CONFIG)"
	@echo "make check         Compile + import checks"
	@echo "make lint          flake8 + mypy"
	@echo "make lint-strict   flake8 + mypy --strict"
	@echo "make clean         Remove caches/temp files"
	@echo "make distclean     Clean + remove output file - $(OUTPUT_FILE)"
	@echo ""

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG) || true

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

check:
	python3 -c "import mazegen; import file_config; import render; import make_output_file"

distclean: clean
	rm -f $(OUTPUT_FILE)
