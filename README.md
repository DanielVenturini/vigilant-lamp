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

## example

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

the ```package.json``` result is:

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

## dependencies
```bash
pip3 install requests
pip3 install semantic_version
pip3 install parsimonious
```

Build on ```Python 3.6```.