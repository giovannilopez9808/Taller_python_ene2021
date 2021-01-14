import os


def files():
    print("Leyendo imagenes")
    files = os.listdir()
    filenames = []
    for file in files:
        if ".png" in file:
            filenames.append(file)
    filenames = sorted(filenames)
    return filenames


def name_format(number, lim):
    size = len(str(lim))-len(str(number))
    name = "0"*size+str(number)
    return name
