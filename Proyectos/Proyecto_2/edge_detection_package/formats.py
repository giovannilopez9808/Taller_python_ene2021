import datetime
import os


def pull_date(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    format = day+"-"+month+"-"+year
    return format


def listdir_sorted(path=""):
    list_sorted = []
    files = os.listdir(path)
    for file in files:
        if (".png" in file) or (".jpg" in file):
            list_sorted.append(file)
    return sorted(list_sorted)


def name_format_kernel(name, kernel_name):
    format_name = name.replace(".jpg", "")
    format_name += "_"+kernel_name+".png"
    return format_name


def jpg2png(name):
    return name.replace(".jpg", ".png")
