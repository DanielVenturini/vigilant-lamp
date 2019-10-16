# vigilant-lamp
Resolve all semver range versions from NPM in ```package.json``` in a specify date.

## Use

add the key ```date``` in package.json:

```json
{
	"date": "2019-01-07"
}
```

but, the follow is better:

```json
{
	"date": "2019-01-07T18:14:39.683Z"
}
```

because this is an NPM time standart.

Then, tipe

```bash
lamp package.json
```

or

```bash
lamp path/to/package.json
```

Then, all dependencies will be downgraded - or upgrade - to best satisfies range in specify date.

## Install

To install, clone this repo and tipe:

```bash
make executable
sudo make install
```

this download all dependencies and install. Be happy.

## Example

If ```package.json``` is:

```json
{
  "date": "2015-06-30",
  "dependencies": {
    "express": "^4.10.6",
    "lodash": "~3.9.0"
  },
  "devDependencies": {
    "mongoose": "^4.5.9",
    "mocha": "2.2.0"
  }
}
```

the command ```lamp package.json``` results in:

```json
{
  "date": "2015-06-30",
  "dependencies": {
    "express": "4.13.0",
    "lodash": "3.9.3"
  },
  "devDependencies": {
    "mocha": "2.2.0",
    "mongoose": "^4.5.9"
  }
}
```

 - ```express``` and ```lodash``` were changed;
 - ```mocha``` wasn't range; and
 - in specify date, ```mongoose@^4.5.9``` didn't exist.

also works to ```peerDependencies```, ```optionalDependencies``` and ```globalDependencies```.

Suport any types of range:
 - "package": "^1.2.3"
 - "package": "~1.2.3"
 - "package": "^1.x"
 - "package": "4.x"
 - "package": "\*"
 - "package": "latest"
 - "package": ">=10"
 - "package": "^2.x < 2.9"
 - "package": "0.x || 10.0.x"
 - ...

## Dependencies
All dependencies are installed when `make executable`.
```bash
pip3 install requests
pip3 install semantic_version
pip3 install parsimonious
pip3 install pyinstaller
pip3 install colorama
pip3 install semver
```

Build on ```Python 3.6```.