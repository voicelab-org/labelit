# How to build sphinx docs

pip install sphinx
pip install sphinx-rtd-theme

cd docs
sphinx-build -b html ./source ./_build
make html
