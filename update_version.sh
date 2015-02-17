## this script updates the version 
## and release a new version (for more info about this is released, have a look at http://danielkummer.github.io/git-flow-cheatsheet/)
git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" cgsdata/__init__.py
rm -rf docs/generated
python setup.py develop
make docs
cd docs && make html && cd ..
git commit docs cgsdata/__init__.py -m "Update to version v$1"
git flow release finish v$1
## python setup.py sdist bdist_wheel upload -r pypi
## python setup.py upload_docs -r pypi
