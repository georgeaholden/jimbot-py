def create_list(filename):
    infile = open(filename)
    target = []
    lines = infile.readlines()
    for line in lines:
        target.append(line.strip())
    infile.close()
    return target


def read_commands():
    infile = open('txts/commands.txt')
    lines = infile.readlines()
    gif_prompt = lines[0].strip()
    help_text = ''
    for line in lines[1:]:
        help_text += line
    help_text = help_text.strip()
    return gif_prompt, help_text


def setup_responses(dictionary):
    infile = open('config.txt')
    lines = infile.readlines()
    for line in lines:
        key, filename = line.strip().split('-')
        dictionary[key] = create_list(filename)
    infile.close()
