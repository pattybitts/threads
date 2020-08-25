def db(header, variable):
    print("\n DEBUG: " + header + ": " + str(variable) + "\n")

def out(variable):
    print(str(variable) + "\n")

def banner(variable):
    print("\n*****\n\n" + str(variable) + "\n\n*****\n")

def file(text, filename):
    archive = open(filename, 'ab')
    archive.write(bytearray(text, 'utf-8'))
    archive.write(bytearray("\n", 'utf-8'))
    archive.close()