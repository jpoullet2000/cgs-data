.PHONY: docs clean build

clean:
	rm -rf cgsdata_env

build:
	virtualenv -p /usr/bin/python cgsdata_env && . cgsdata_env/bin/activate && \
	pip install -r requirements.txt

docs:
	sphinx-apidoc -F -o docs cgsdata > /dev/null
