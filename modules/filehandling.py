def create_list(filename, start=0):
    infile = open(filename)
    target = []
    lines = infile.readlines()
    for line in lines[start:]:
        if line.startswith('#'):
            continue
        target.append(line.strip())
    infile.close()
    return target


def read_commands():
    infile = open('config_txts/commands.txt')
    lines = infile.readlines()
    gif_prompt = lines[0].strip()
    help_text = ''
    for line in lines[1:]:
        help_text += line
    help_text = help_text.strip()
    return gif_prompt, help_text


def setup_strings_dict(dictionary):
    infile = open('config.txt')
    lines = infile.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        key, filename = line.strip().split('-')
        dictionary[key] = create_list(filename)
    infile.close()


def get_contents(filename):
    infile = open(filename)
    result = infile.read()
    return result.strip()


if __name__ == '__main__':
    print(create_list('../phrase_txts/hello_responses.txt'))