import os
import heapq
import pickle



class HuffmanCoding:

    #Constractor 
    def __init__(self,path):
        self.path = path
        self.min_heap = []
        self.codes = {}
        self.reverse_mapping = {}
    

    #MinHeap Node
    class HeapNode:
        def __init__(self,char,freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        #comparator
        def __lt__(self,other):
            return self.freq < other.freq

        def __eq__(self,other):
            if(other==None):
                return False
            
            if(not isinstance(other, HeapNode)):
               return False

            return self.freq == other.freq
   
   #Function to get frequency
    def get_frequency(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character]=0

            frequency[character] += 1
        return frequency
   

   #pushing frequency into MinHeap
    def make_heap(self, frequency):
        
        for key in frequency:
            node=self.HeapNode(key,frequency[key])
            heapq.heappush(self.min_heap,node)

   
   #creating heap tree by merging frequency 
    def merge_freqs(self):
        while(len(self.min_heap)>1):
            node1=heapq.heappop(self.min_heap)
            node2=heapq.heappop(self.min_heap)

            merged=self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.min_heap, merged)


    #recursively traversing heap to get code
    def get_code_helper(self, root, temp):
        if(root==None):
            return
        
        if(root.char != None):
            self.codes[root.char] = temp
            self.reverse_mapping[temp] = root.char
            return

        self.get_code_helper(root.left,temp+"0")
        self.get_code_helper(root.right,temp+"1")

    #function to get code for character
    def get_codes(self):
        root =heapq.heappop(self.min_heap)
        temp=""

        self.get_code_helper(root,temp)


    #replacing character with codes
    def get_encoded_text(self, text):
        encoded_text=""

        for character in text:
            encoded_text+=self.codes[character]

        return encoded_text


    #paddind extra bits to make it multiple of *
    def pad_encodedtext(self,encoded_text):
        add_padding = 8 - len(encoded_text)%8 

        for i in range(add_padding):
            encoded_text+="0"

        padding_info="{0:08b}".format(add_padding)
        encoded_text=padding_info + encoded_text

        return encoded_text

    #converting bits into byte
    def get_byte_arr(self, padded_encoded_text):
        b=bytearray()

        for i in range(0,len(padded_encoded_text), 8):
            byte=padded_encoded_text[i:i+8]
            b.append(int(byte,2))

        return b


    # compresor
    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        if (file_extension != ".txt"):
            return f"{file_extension} cannot be compressed...Select '.txt' file to compress"
        output_path = filename + ".bin"

        with open(self.path,'r+') as file, open(output_path,'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.get_frequency(text)

            self.make_heap(frequency)
            self.merge_freqs()
            self.get_codes()

            encoded_text=self.get_encoded_text(text)
            padded_encoded_text=self.pad_encodedtext(encoded_text)

            b=self.get_byte_arr(padded_encoded_text)
            output.write(bytes(b))

            with open(f"{filename}.pkl","wb") as rev_map_file:
                pickle.dump(self.reverse_mapping, rev_map_file)

        print("compressed")
        return output_path



    #function to remove extra padding we added
    def remove_padding(self, bit_string):
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)

        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1*extra_padding]

        return encoded_text



    #replacing codes with their assigned character 
    def decoding(self,encoded_text):
        temp=""
        decoded_text=""

        for bit in encoded_text:
            temp+=bit

            if(temp in self.reverse_mapping):
                character=self.reverse_mapping[temp]
                decoded_text+=character
                temp=""

        return decoded_text


    #decompressing
    def decompress(self):
        filename, file_extension=os.path.splitext(self.path)
        if(file_extension != ".bin"):
            return f"{file_extension} cannot be decompressed...Select '.bin' file to decompress"
        
        output_path=filename+"_decompressed"+".txt"

        with open(f"{filename}.pkl","rb") as rev_map_file:
            self.reverse_mapping = pickle.load(rev_map_file)

        
        with open(self.path, 'rb') as file, open(output_path,'w') as output:
            bit_string=""

            byte=file.read(1)
            while(len(byte)>0):
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)

            encoded_text=self.remove_padding(bit_string)

            decoded_text=self.decoding(encoded_text)

            output.write(decoded_text)

        print("Decompressed")
        return output_path 

        