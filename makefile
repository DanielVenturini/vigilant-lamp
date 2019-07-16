all: deps executable install

install:
	cp dist/lamp/* /usr/bin/ -r

executable:
	pyinstaller lamp.py -y

deps:
	pip3 install requests
	pip3 install semantic_version
	pip3 install parsimonious
	pip3 install pyinstaller
	pip3 install semver