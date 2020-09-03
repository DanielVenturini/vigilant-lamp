all: deps executable

deps:
	pip3 install -r requirements.txt

install:
	cp dist/main /usr/bin/lamp -r

executable:
	pyinstaller main.py -y --onefile

test:
	git checkout test/package.json
	python3 test/test_python.py

clean:
	rm -r build/
	rm -r dist/
	rm main.spec