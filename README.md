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
pip install semver
pip install requests
```

or use

```bash
pip3
```

Build on ```Python 3.7```.