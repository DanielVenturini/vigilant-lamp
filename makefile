all: deps executable install

deps:
	pip3 install -r requirements.txt

install:
	cp dist/lamp/* /usr/bin/ -r

executable: deps
	pyinstaller lamp.py -y