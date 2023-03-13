import os
import sys
import glob
import signal
import hashlib


def keyboard_interrupt(signal, frame):
    print("\nExiting")
    sys.exit(0)


signal.signal(signal.SIGINT, keyboard_interrupt)


def getmd5(fname):
    md5 = hashlib.md5()
    with open(fname, "rb") as f:
        data = f.read()
        datamd5 = hashlib.md5(data)
    return datamd5.hexdigest()


def concatNames(path, folder):
    if(path[-1] != "/"):
        path += "/"
    fullPath = "" + path + folder
    return(fullPath)


def removeDups(recursive, silent, path, r):
    folders = []

    try:
        os.chdir(path)
    except:
        sys.exit("No folder received. Exiting")

    existingfiles = glob.glob("*")
    file_hashes = []
    duplicates = []

    for f in existingfiles:
        try:
            if getmd5(f) in file_hashes:
                duplicates.append(f)
            else:
                file_hashes.append(getmd5(f))
        except IsADirectoryError:
            if(not silent and not recursive):
                print("Skipping", f)
            if(recursive):
                # folders.append(concatNames(path, f))
                removeDups(recursive, silent, concatNames(path, f), r+1)
                os.chdir(path)
            continue

    print("There are ", len(duplicates), " duplicates.")

    if(not silent):
        for d in duplicates:
            print(d)

    if len(duplicates) == 0:
        sys.exit("No duplicates found. Exiting.")
    print("\nThere are", len(duplicates), "duplicates in", path)
    choice = input("Are you sure you want to delete all duplicates in the current folder? [Y|n] ")
    while choice not in ("yes", "no", "Yes", "No", "Y", "N", "y", "n", ""):
        choice = input("Are you sure you want to delete all duplicates in the current folder? [Y|n] ")
    if choice in ("no", "No", "N", "n" and r == 0):
        sys.exit("Exiting")
    elif choice in ("yes", "Yes", "Y", "y", ""):
        print("Removing duplicate files in the current directory")
        for d in duplicates:
            os.remove(d)


def helpDups():
    print()
    print("Usage: ")
    print("     rmdups [OPTIONS] [PATH TO FOLDER]")
    print()
    print("Options: ")
    print("     'help': print this screen")
    print("     'silent': do not print file names")
    print("     'recursive': check folders within given path")
    print()


def main(argv):
    if "help" in argv:
        helpDups()
    else:
        recursive = False
        silent = False

        if("recursive" in argv):
            recursive = True
        if("silent" in argv):
            silent = True
        try:
            path = argv[-1]
        except:
            sys.exit("No folder received. Exiting")

        removeDups(recursive, silent, path, 0)


if __name__ == "__main__":
    main(sys.argv[1:])
