"""I keep forgetting to update the version field in all required places whenever I change something, so this script
should remove the mental burden. Accurate version field should always be in config.ini"""

import configparser
import re

VERSION_REGEX = "\d+.\d+.\d+"


def update_readme(version):
    """Updates the README.md file to a new given version"""
    try:
        infile = open("../README.md")
        lines = infile.readlines()
        infile.close()
        old = lines[1].lstrip("### ")
        lines[1] = "### {}\n".format(version)
        infile = open("../README.md", "w")
        infile.writelines(lines)
        infile.close()
        print("Updated version field in README.md from {} to {}".format(old, version))
    except:
        print("Unable to update version field in README.md")


def update_changelog(version):
    """Updates the changelog.txt file to a new given version"""
    try:
        infile = open("../changelog.txt")
        lines = infile.readlines()
        infile.close()
        lines[0] = re.sub(VERSION_REGEX, version, lines[0])
        infile = open("../changelog.txt", "w")
        infile.writelines(lines)
        infile.close()
        print("Updated version field in changelog.txt, field now reads")
    except:
        print("Unable to update version field in changelog.txt")


def main():
    config = configparser.ConfigParser()
    config.read("../config.ini")
    version = config["DEV"]["version"]
    update_readme(version)
    update_changelog(version)


main()
