import heapq
import binascii

class node:
    def __init__(self, val=None, freq=0, right=None, left=None, code=None):
        if val is None:
            self.is_internal = True
            self.val = None
        else:
            self.val = val
            self.is_internal = False
        self.freq = freq
        self.right= right
        self.left = left
        self.code = None

    def get_val(self):
        return self.val

    def get_frequency(self):
        return self.freq
    
    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def __lt__(self, other):
        return self.freq < other.freq
        

def getFrequencies(fname):
    f = open(fname, "rb")
    #s = f.readline()
    data = f.read()
    f.close()
    freq = {}
    for c in data:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq

def create_heap(freq):
    nodes = []
    for key in freq:
        if freq[key] != 0:
            heapq.heappush(nodes, node(val=key, freq=freq[key]))
    return nodes

def create_tree(freq):
    heap = create_heap(freq)
    while len(heap) != 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        total_freq = node1.get_frequency() + node2.get_frequency()
        new_node = node(freq=total_freq, left=node1, right=node2)
        heapq.heappush(heap, new_node)
    return heap

def traverse_tree(tree, beginning=''):
    if tree.left == None and tree.right == None:
        #print(beginning + ' = ' + str(chr(tree.get_val())))
        tree.set_code(beginning)
        return
    elif tree.left == None:
        traverse_tree(tree.right, beginning+'1')
    elif tree.right == None:
        traverse_tree(tree.left, beginning+'0')
    else:
        traverse_tree(tree.right, beginning+'1')
        traverse_tree(tree.left, beginning+'0')

def get_codes(freq):
    tree = create_tree(freq)

    traverse_tree(tree[0])
    if tree[0].left == None and tree[0].right == None:
        tree[0].set_code('0')
    return get_codes_helper(tree[0])

def get_codes_helper(tree, codes={}):
    if tree.left == None and tree.right == None:
        codes[tree.get_val()] = tree.get_code()
        return codes
    elif tree.left == None:
        codes = get_codes_helper(tree.right, codes)
    elif tree.right == None:
        codes = get_codes_helper(tree.left, codes)
    else:
        codes = get_codes_helper(tree.left, codes)
        codes = get_codes_helper(tree.right, codes)
    return codes

def get_codes_from_arr(arr):
    pass

def construct_header(codes):
    header = ''
    for key in codes:
        #header += str(chr(key)) + ',' + str(codes[int(key)]) + ','
        header += str(key) + ',' + str(codes[key]) + ','
    header = header[:-1]
    
    return header

def extract_header_text(file_content):
    header = ''
    file_content = str(file_content)
    for i in range(2, len(file_content)):
        print('i = ' + str(i))
        print('file_content[i] = ' + str(file_content[i]))
        if file_content[i] == '\\' and file_content[i+1] == 'n':
            if i + 2 < len(file_content) and file_content[i+2] == ',':
                header += str(file_content[i])
            else:
                #print('Returning..')
                #print('header = ' + header)
                return header, file_content[i+1:]
        header += str(file_content[i])
            

def get_compressed_content(compressed_content):
    length = len(compressed_content)
    #print('number of bits = {}'.format(length))
    rem = length % 8
    #print('number of padded zeros = {}'.format((8-rem)%8))
    length = length + (8 - rem) % 8
    for i in range((8-rem)%8):
        compressed_content = '0' + compressed_content
    #print('Content after zero padding: {}\nLength after zero padding: {}'.format(compressed_content, length))
    num_words = length / 8
    num_words = int(num_words)
    total_content = ''
    #print('num_words = ' + str(num_words))
    for i in range(num_words):
        #print('i = ' + str(i))
        #print('compressed_content[i*8:i*8+8] = ' + compressed_content[i * 8:i * 8 + 8])
        ch = int(compressed_content[i * 8:i * 8 + 8], 2)
        #print('ch = "' + str(chr(ch)) + '"')
        total_content += str(chr(ch))
    return total_content


def compress_file(fname, codes):
    f1 = open(fname + '_compressed', 'wb')
    f2 = open(fname, 'rb')
    data = f2.read()
    f2.close()

    compressed_file = ''

    header = construct_header(codes)
    #print('len(data) = {}'.format(len(data)))
    for c in data:
        try:
            #print('{} = {}'.format(c, codes[c]))
            compressed_file += codes[c]
        except:
            print('Key: {} not found'.format(int(c)))
    #print('header: ' + header)
    rem = len(compressed_file) % 8
    padded_zeros = (8 - rem) % 8;
    header += '\n' + str(padded_zeros) + '\n'
    compressed_content = get_compressed_content(compressed_file)
    size_woheader = len(compressed_content)
    #print(compressed_file.encode('utf-8'))
    #print('len(compressed_file) = ' + str(len(compressed_file)))
    compressed_file = header + compressed_content
    size_wheader = size_woheader + len(header)
    #print(compressed_file.encode("utf-8"))
    f1.write(bytearray(compressed_file, encoding='utf-8'))
    f1.close()
    f2.close()

    return size_wheader, size_woheader

    return 


def reverse_code(codes):
    reversed_codes = {}
    for key in codes:
        reversed_codes[codes[key]] = key
    return reversed_codes
        

def build_reverse_codes(arr):
    dic = {}
    for i in range((int)(len(arr)/2)):
        #print('dic[arr[2*i+1]] = {}'.format(arr[2*i]))
        dic[arr[2*i+1]] = arr[2*i]
    return dic

def decompress_file(fname, codes=None):
    f1 = open(fname, 'rb')
    fname.replace("_compressed", '')
    f2 = open(fname +'_2', 'wb')

    #print("=============Decompressing=================")
    s1 = f1.readline()
    s1 = s1.decode('utf-8')
    s1 = s1[:-1]
    #print('s1 = {}'.format(s1))
    arr = s1.split(',')
    #print('len(arr) = {}'.format(len(arr)))
    #print('len(s1) = {}'.format(len(s1)))
    
    #print('len(arr) = ' + str(len(arr)))
    #for key in codes:
        #print('{} = {}'.format(key, codes[key]))
    s1 = f1.readline()
    s1 = s1.decode('utf-8')
    if s1[0] == ',':
        arr = arr + s1.split(',')
        s1 = f1.readline()
    
    #print('len(arr) = {}'.format(len(arr)))

    codes = build_reverse_codes(arr)
    #for key in codes:
    #    print(str(key) + ' = ' + str(codes[key]))
    
    padded_zeros = int(s1)
    #print('padded_zeros = {}'.format(padded_zeros))
    current_str = ''
    s1 = f1.readline()
    while s1 != b'':
        s1 = s1.decode('utf-8')
        for i in range(len(s1)):
            x = format(ord(s1[i]), '08b')
            current_str += x
        s1 = f1.readline()

    #print('len(current_str) = ' + str(len(current_str)))
    #print('leading_zeros = ' + str(leading_zeros))
    current_str = current_str[padded_zeros:]
    #print(current_str)

    current_letter = ''
    decompressed_text = ''
    for i in range(len(current_str)):
        current_letter += current_str[i]
        if current_letter in codes:
            try:
                c = codes[current_letter]
                c = int(c, 10)
                decompressed_text += chr(c)
            except:
                print('Key {} not found!'.format(current_letter))
            current_letter = ''
    byts = bytearray(decompressed_text, encoding='utf-8')
    #print('len(bytes) = {}'.format(len(bytes)))
    f2.write(byts)
    #print('len(decompressed_text) = {}'.format(len(decompressed_text)))
    #print(decompressed_text)

    f1.close()
    f2.close()
