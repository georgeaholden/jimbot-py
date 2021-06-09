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


def get_contents(filename):
    """Returns the entire contents of a given file as a string, with trailing whitespace removed"""
    infile = open(filename)
    result = infile.read()
    infile.close()
    return result.strip()


def get_contents_as_list(filename):
    """Returns the contents of a given file as a list of lines, with trailing whitespace removed"""
    infile = open(filename)
    lines = infile.readlines()
    result = []
    for line in lines:
        result.append(line.strip())
    infile.close()
    return result


if __name__ == '__main__':
    print(create_list('../phrase_txts/hello_responses.txt'))