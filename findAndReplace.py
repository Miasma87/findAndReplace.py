#! /usr/bin/python

import os
import fnmatch
import sys


def ask_validation(question, default="no"):
    valid = {"yes": True,   "y": True,
             "no": False,   "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def searchFile(directory, word_to_find, filePattern, FoD):
    gotIt = False
    lineNb = 0
    path = os.getcwd() + '/' + directory
    if FoD is False:  # Is a directory
        for path, dirs, files in os.walk(os.path.abspath(path)):
            for filename in fnmatch.filter(files, filePattern):
                filepath = os.path.join(path, filename)
                with open(filepath) as openfile:
                    for line in openfile:
                        for part in line.split():
                            if word_to_find in part:
                                print filepath
                                print line
                                gotIt = True
                                lineNb += 1
    else:  # Is a file
        with open(path) as openfile:
            for line in openfile:
                for part in line.split():
                    if word_to_find in part:
                        print path
                        print line
                        gotIt = True
                        lineNb += 1
    return gotIt, lineNb


def findReplace(directory, find, replace, filePattern, FoD):
    path = os.getcwd() + '/' + directory
    if FoD is False:  # Is a directory
        for path, dirs, files in os.walk(os.path.abspath(path)):
            for filename in fnmatch.filter(files, filePattern):
                filepath = os.path.join(path, filename)
                with open(filepath) as f:
                    s = f.read()
                s = s.replace(find, replace)
                with open(filepath, "w") as f:
                    f.write(s)
    else:  # Is a file
                with open(path) as f:
                    s = f.read()
                s = s.replace(find, replace)
                with open(path, "w") as f:
                    f.write(s)


def main():
    print
    if len(sys.argv) < 3:
        print "Arguments missing!"
        print "findAndReplace.py `a file or a directory`"
        " `word to find` `replace by` `filetype`"
        exit(-1)
    else:
        if len(sys.argv) == 4:
            filetype = "*"
        else:
            filetype = "*." + sys.argv[4]

    if os.path.isfile(sys.argv[1]):
        type_FoD = True  # Is a file
    else:
        type_FoD = False  # Is a directory

    anything, line = searchFile(sys.argv[1], sys.argv[2], filetype, type_FoD)
    if anything is True:
        print "`%s` found %d times" % (sys.argv[2], line)
        print "You will replace `%s` by `%s` in `%s` for `%s` files"
        "" % (sys.argv[2], sys.argv[3], sys.argv[1], filetype)
        answer = ask_validation("Do you want to change these files?")
        if answer is True:
            findReplace(sys.argv[1],
                        sys.argv[2],
                        sys.argv[3],
                        filetype,
                        type_FoD)
        else:
            pass
    else:
        print "No match"

main()
