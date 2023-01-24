import tkinter as tk
from HuffmanCoding import HuffmanCoding
from tkinter import filedialog

path=""



#making window
window=tk.Tk()
window.title("Huffman Coding")
canvas=tk.Canvas(window, width=800 , height=600 , bg='skyblue')
canvas.grid(columnspan=10, rowspan=10)
window.resizable(False,False)


#Heading
heading=tk.Label(window, text="Text File Compressor",bg="skyblue", font=("Arial Bold",18))
heading.grid(columnspan=6, row=0, column=2)


#Browse Button
browse_button=tk.Button(window, text="Browse", command=lambda:get_file(), bg="black", fg="white", height=3, width=15)
browse_button.grid(columnspan=3,row=3,column=2)


#Compress Button
compress_button=tk.Button(window, text="Compress", command=lambda:compress_file(), bg="black", fg="white", height=3, width=15)
compress_button.grid(columnspan=3,row=3,column=4)


#Decompress Button
decompress_button=tk.Button(window, text="Decompress", command=lambda:decompress_file(), bg="black", fg="white", height=3, width=15)
decompress_button.grid(columnspan=3,row=3,column=6)


#Creating Text Box
text_box = tk.Text(window, height=10, width=90)
text_box.insert(1.0, "Select Your Text/Bin File For Compressing/Decompressing")
text_box.tag_configure("center", justify="center")
text_box.tag_add("center", 1.0, "end")
text_box.grid(columnspan=3,column=4, row=2)





#printing path in output
def show_output(output):
    text_box.delete(1.0, "end")
    text_box.insert(1.0, output)

#geting the input file
def get_file():
    global path
    path = ""
    file=filedialog.askopenfilename(parent=window, title="Select a file")
    path=file

    
    output= "Selected file -> " + path

    show_output(output)
    


#compressing file by calling HuffmanCoding 
def compress_file():
    h=HuffmanCoding(path)
    output="Compressed File-> " + h.compress()
    show_output(output)


#decompressing file by calling HuffmanCoding
def decompress_file():
    h=HuffmanCoding(path)
    output="Dcompressed File-> " + h.decompress()
    show_output(output)



window.mainloop()

