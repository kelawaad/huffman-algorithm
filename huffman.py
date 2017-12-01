def getFrequencies(fname):
    f = open("test.txt", "r")
    s = f.readline()

    freq = {}

    while s != "":
        length = len(s)
        for i in range(length):
            if s[i] in freq:
                freq[s[i]] += 1
            else:
                freq[s[i]] = 1 
        s = f.readline()

    return freq



freq = getFrequencies("test.txt")
for key in freq:
    if freq[key] != 0:
        print(str(key) + " = " + str(freq[key]))