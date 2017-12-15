import myfuncs
import time
import os

def getAllFiles(path):
    files = []
    if not os.path.isdir(path):
        files.append(path)
        return files

    for x in os.listdir(path):
        if os.path.isdir(path + '/' + x):
            files += getAllFiles(path + '/' + x)
        else:
            files.append(path + '/' + x)
    return files


#os.path.isdir(path)    returns true if path is a folder
#os.path.exists(path)   return true if file/folder exists

files = getAllFiles('empty')
for f in files:
    print(f)
fname = 'abc'
freq = myfuncs.getFrequencies(fname)
codes = myfuncs.get_codes(freq)
max_len = 0
for key in codes:
    if len(codes[key]) > max_len:
        max_len = len(codes[key])

print('Byte\t{:^8}\tNew Code'.format('Code'));
for key in sorted(codes):
    print('{0:>3}\t{1:08b}\t{2:>{3}}'.format(key, key, codes[key], max_len))

total = 0
for key in freq:
    total += freq[key]

print(total)

start = time.time()
size_wheader, size_woheader = myfuncs.compress_file(fname, codes)
end = time.time()
print('size with header = {}\nsize without header = {}'.format(size_wheader, size_woheader))

print("Compression ratio = {}".format(size_wheader/total))

print('Time Elapsed = {}ms'.format((end - start) * 1000))

myfuncs.decompress_file(fname + '_compressed')
