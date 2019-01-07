# vigilant-lamp
Resolve all semver range versions from NPM in ```package.json``` in a specify date.

## Use

add the key ```date``` in package.json:

```json
{
	"date": "2019-01-07"
}
```

Then, tipe

```bash
lamp package.json
```

or

```bash
lamp path/to/package.json
```

## dependencies
```bash
pip install semver		# semver-2.8.1
pip install requests	# requests-2.21.0 urllib3-1.24.1
```

or use

```bash
pip3
```

Build on ```Python 3.6```.