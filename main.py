import re
from ruamel.yaml import YAML

yaml=YAML()
yaml.width=float("inf")
yaml.preserve_quotes = False
yaml.compact(seq_seq=False, seq_map=False)

def write_redacted(redacted):
    """ secrets_redacted.yaml """

    # match triple brackets
    regex_pattern = r"\[{3}[^\]]+?\]{3}"

    # read "secrets_template.yaml"
    template_dict = read(TEMPLATE)

    # substitute secrets with "REDACTED"
    for key, value in template_dict.items():
        redact = re.sub(regex_pattern, "REDACTED", str(value))
        template_dict.update({key: redact})

    # write "secrets_redacted.yaml"
    write(redacted, template_dict)

def write_secrets(secrets):
    """ secrets.yaml """

    # read "secrets_template.yaml"
    template_dict = read(TEMPLATE)

    # remove triple brackets
    for key, value in template_dict.items():
        redact = value.replace("[[[", "").replace("]]]", "")

        # update value with type
        if is_float(redact):
            value = float(redact)
        elif redact.isdigit():
            value = int(redact)
        else:
            value = str(redact)
        template_dict.update({key: value})

    # write "secrets.yaml"
    write(secrets, template_dict)

def is_float(string):
    """ type check """
    try:
        return float(string) and '.' in string
    except ValueError:
        return False

def read(input_file):
    """ read file """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return yaml.load(file)
    except FileNotFoundError:
        print(f'File not found: "{input_file}"')
        exit(1)

def write(output_file, content):
    """ write file """
    with open(output_file, "w", encoding="utf-8") as outfile:
        yaml.dump(content, outfile)

TEMPLATE = "/Users/matte/mount/hass-config/secrets_template.yaml"
write_redacted("/Users/matte/mount/hass-config/secrets_redacted.yaml")
write_secrets("/Users/matte/mount/hass-config/secrets.yaml")

print("ok")
