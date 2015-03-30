# We only need to import this module
import os.path
# The top argument for walk.
topdir = '/home/ilya/_testing'
# The arg argument for walk, and subsequently ext for step
exten = ''


def step(ext, dirname, names):
    ext = ext.lower()

    for name in names:
        if name.lower().endswith(ext):
            n = str(os.path.join(dirname, name))
            f = open(n, 'rb')
            print(f.read())
            f.close()

# Start the walk
os.path.walk(topdir, step, exten)
