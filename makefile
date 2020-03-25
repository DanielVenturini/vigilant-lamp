all: deps executable

deps:
	pip3 install -r requirements.txt

install:
	cp dist/lamp /usr/bin/ -r

executable:
	pyinstaller lamp.py -y --onefile

clean:
	rm -r build/
	rm -r dist/
	rm lamp.spec