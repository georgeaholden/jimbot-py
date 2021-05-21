"""Contains functions that handle the manipulation of files"""


def create_list(filename, start=0):
    """Returns a list of all the lines in a given file with trailing whitespace removed. Optional start index"""
    infile = open(filename)
    result = []
    lines = infile.readlines()
    for line in lines[start:]:
        if line.startswith('#'):
            continue
        result.append(line.strip())
    infile.close()
    return result


def read_commands():
    """Reads the super ugly command txt, which contains the gif prompt in it's first line and help_text"""
    infile = open('config_txts/commands.txt')
    lines = infile.readlines()
    gif_prompt = lines[0].strip()
    help_text = ''
    for line in lines[1:]:
        help_text += line
    help_text = help_text.strip()
    return gif_prompt, help_text


def read_config(dictionary):
    """Extracts data from config.txt. Currently updates the given dictionary in place, and returns a string containing
    the version number, which is super gross. Eventually version should be stored elsewhere"""
    infile = open('config.txt')
    lines = infile.readlines()
    for line in lines[1:]:
        if line.startswith('#'):
            continue
        key, filename = line.strip().split('-')
        dictionary[key] = create_list(filename)
    infile.close()
    return lines[0].strip()


def get_contents(filename):
    """Returns the entire contents of a given file as a string, with trailing whitespace removed"""
    infile = open(filename)
    result = infile.read()
    infile.close()
    return result.strip()


if __name__ == '__main__':
    print(create_list('../phrase_txts/hello_responses.txt'))