# Uses LSB

from PIL import Image
import sys
import argparse
import numpy as np
import typing

def dec_to_binary(num: int, index: int) -> str:
    subtraction_list: List[int] = [128, 64, 32, 16, 8, 4, 2, 1]
    current_str: str = ""
    # returns if the index value is out of range.
    if index > 7:
        return current_str

    if (num - subtraction_list[index]) >= 0:
        # adds a 1 if the number can be subtracted.
        num = num - subtraction_list[index]
        current_str += "1"
        current_str += dec_to_binary(num, index + 1)
    else:
        # adds a 0 if the number cant be subtracted.
        current_str += "0"
        current_str += dec_to_binary(num, index + 1)
        
    return current_str


def binary_to_dec(binary: str) -> int:

    return int(binary, 2)


def modify_bit(n: int, p: int, b: int):
    mask = 1 << p
    return (n & ~mask) | ((b << p) & mask)


def get_code(path: str) -> str:
    encoded_text = ""
    with Image.open(path) as image:
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(image.getpixel((x, y)))
                for n in range(0, 3):
                    encoded_text += str(pixel[n] & 1)
    # Returns the string.
    return encoded_text


def return_true_code(binary_list, delim: str) -> str:
    text = ""
    for item in binary_list:
        text += chr(binary_to_dec(item))
        if text.__contains__(delim):
            return text[0:-len(delim)]




if __name__ == "__main__":
    # Creates the parser
    parser = argparse.ArgumentParser(prog="imagesteg", description="Hides data within the specified image.")
    # Add the arguments
    parser.add_argument("choice", metavar="choice", type=str, help="Choice whether to decode/encode an image.")
    parser.add_argument("path", metavar="path", type=str, help="The path to the image.")
    parser.add_argument("delimiter", metavar="delimiter", type=str, help="The delimiter for the message. You need this for encoding/decoding.")
    parser.add_argument("--text", metavar="text", type=str, help="The text you want to hide inside the image.")
    
    args = parser.parse_args()

    delim = args.delimiter
    choice = args.choice.lower()
    path = args.path
    text = args.text
    im = Image.open(path, 'r')

    if choice == "encode" and text == None:
        print("Please enter the text you want to encode.")
        sys.exit()
    
    if choice == "encode":
        text += delim
        # converts all the characters to their binary equivalents 
        bin_text = [dec_to_binary(ord(char), 0) for char in text]
        new_bin = []
        for item in bin_text:
            for char in item:
                new_bin.append(char)

        binary_string = "".join(new_bin)

        counter = 0
        with Image.open(path) as image:
            width, height = image.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(image.getpixel((x, y)))
                    for n in range(0, 3):
                        if(counter < len(binary_string)):
                            pixel[n] = modify_bit(pixel[n], 0, int(binary_string[counter]))
                            counter += 1

                    image.putpixel((x, y), tuple(pixel))
            image.save("encoded_" + path, "PNG")
            image.show()


    elif choice == "decode":
        
        encoded_text = get_code(path)
        binary_list = [encoded_text[i:i+8] for i in range(0, len(encoded_text), 8)]
        print(return_true_code(binary_list, delim))
