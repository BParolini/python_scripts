#!/usr/bin/env python

import os
import sys
from mutagen.id3 import ID3


def save_folder_jpg(mp3_file):
    file = open(mp3_file, 'rb')
    mp3 = ID3(file)
    apic_data = mp3.getall("APIC")
    if len(apic_data) >= 1:
        image_file = open(os.path.join(os.path.dirname(mp3_file), "folder.jpg"), "w+b")
        image_file.write(apic_data[0].data)
        image_file.close()


def navigate_directory(directory):
    print("Navigating to: ", directory)
    sub_directory = ""
    for directory_name in os.listdir(directory):
        sub_directory = os.path.join(directory, directory_name)
        if os.path.isdir(sub_directory):
            navigate_directory(sub_directory)
        else:
            if find_folder_jpg(directory):
                return

    if sub_directory.endswith(".mp3"):
        save_folder_jpg(sub_directory)


def find_folder_jpg(directory):
    for file in os.listdir(directory):
        if file == "folder.jpg":
            return True

    return False


if __name__ == "__main__":
    navigate_directory(sys.argv[1])
