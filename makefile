all: deps executable install

install:
	cp dist/lamp/* /usr/bin/ -r

executable:
	pyinstaller lamp.py -y