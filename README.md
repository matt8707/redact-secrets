# redact-secrets

Redacts [Home Assistant](https://github.com/home-assistant/core) secrets for public repositories.

## But, why?

I'm sharing my configuration publicly and I want to include my commands but not actual secrets like tokens. It's a pain to have to redact secrets manually.

## Usage

The `secrets_template.yaml` is read and writes two files:

* `secrets.yaml` file read by hass
* `secrets_redacted.yaml` file pushed to your repository



You also have to edit the paths in `main.py`

```python
TEMPLATE = "/Users/matte/mount/hass-config/secrets_template.yaml"
write_redacted("/Users/matte/mount/hass-config/secrets_redacted.yaml")
write_secrets("/Users/matte/mount/hass-config/secrets.yaml")
```

## Example

*Note: If the secret starts with brackets you have to wrap it in quotes.*

#### secrets_template.yaml

```yaml
token: "[[[Gffk52sd5]]]"
command: my cool command but hide my [[[password]]]
remote: ssh [[[matt@142.250.181.238]]] reboot
```

#### secrets_redacted.yaml

```yaml
token: REDACTED
command: my cool command but hide my REDACTED
remote: ssh REDACTED reboot
```

#### secrets.yaml

```yaml
token: Gffk52sd5
command: my cool command but hide my password
remote: ssh matt@142.250.181.238 reboot
```

#### .gitignore

```text
secrets.yaml
secrets_template.yaml
```


## Terminal

Edit `~/.zshrc` and add the function

```bash
makes() {
   python3 "/Users/matte/GitHub/redact-secrets/main.py"
}
```

Now you can type `makes` into terminal to quickly generate the files.

## Disclaimer

Please double-check `secrets_redacted.yaml` before you push it so you don't leak any sensitive information.
