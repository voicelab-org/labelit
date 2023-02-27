update-main:
	# requirements.txt
	pip-compile $(PIP_COMPILE_OPTIONS) --verbose --upgrade --no-header --output-file .requirements.txt
	echo "# Generated $(shell date +'%F %T.%N')" > requirements.txt
	echo "# =======================================" >> requirements.txt
	echo "" >> requirements.txt
	cat .requirements.txt | grep -v "^--index-url" | grep -v "^--extra-index-url" >> requirements.txt
	rm .requirements.txt

update-dev:
	# requirements-dev.txt
	pip-compile $(PIP_COMPILE_OPTIONS) --extra "dev" --upgrade --no-header --output-file .requirements-dev.txt
	echo "# Generated $(shell date +'%F %T.%N')" > requirements-dev.txt
	echo "# =======================================" >> requirements-dev.txt
	echo "" >> requirements-dev.txt
	cat .requirements-dev.txt | grep -v "^--index-url" | grep -v "^--extra-index-url" >> requirements-dev.txt
	rm .requirements-dev.txt

update:
	make -j 2 update-main update-dev
