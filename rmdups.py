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


def removeDups(argv):
    if not argv[0]:
        sys.exit("No folder received. Exiting")
    os.chdir(argv[0])
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
            print("Skipping", f)
            continue
    print("There are ", len(duplicates), " duplicates.")
    for d in duplicates:
        print(d)
    if len(duplicates) == 0:
        sys.exit("No duplicates found. Exiting.")
    print("\nThere are ", len(duplicates), " duplicates.")
    choice = input("Are you sure you want to delete all duplicates in the \
        current folder? [Y|n] ")
    while choice not in ("yes", "no", "Yes", "No", "Y", "N", "y", "n", ""):
        choice = input("Are you sure you want to delete all duplicates in \
            the current folder? [Y|n] ")
    if choice in ("no", "No", "N", "n"):
        sys.exit("Exiting")
    print("Removing duplicate files in the current directory")
    for d in duplicates:
        os.remove(d)


def main(argv):
    removeDups(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
