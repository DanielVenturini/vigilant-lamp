all: deps executable install

pre:
	make deps
	make executable

install:
	cp dist/lamp/* /usr/bin/ -r

executable:
	pyinstaller lamp.py

deps:
	pip3 install requests
	pip3 install semantic_version
	pip3 install parsimonious
	pip3 install pyinstaller