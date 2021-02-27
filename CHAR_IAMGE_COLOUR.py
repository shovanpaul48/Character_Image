import argparse
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps

######################## BASIC LEBELS((PARAMETERS) #####################################################
def get_args(filename,newfilename):
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default=filename)
    parser.add_argument("--background", type=str, default="black", choices=["black", "white", "gray"])
    parser.add_argument("--output", type=str, default=newfilename)
    parser.add_argument("--mode", type=str, default="small", choices=["capital", "small","digit","all"])  ##### SET DEFAULT
    parser.add_argument("--num_cols", type=int, default=500)    ### SET COLOUMN
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()
    return args

########################## DIFFERENT TYPES OF CHARACTER #####################################
def main(opt):
    if opt.mode == "capital":
        CHAR_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    elif opt.mode == "small":
        CHAR_LIST = "abcdefghijklmnopqrstuvwxyz"
    elif opt.mode == "digit":
        CHAR_LIST = "0123456979"
    elif opt.mode == "all":
        CHAR_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456979`,~,@#$%^&*()_-+=*/.{}[];:<>,.?/ "
    
########################## BACKGROUND COLOR OF #############################################
    if opt.background == "black":
        bg_code = (0, 0, 0)
    elif opt.background == "white":
        bg_code = (255, 255, 255)
    elif opt.background == "gray":
        bg_code = (255, 209, 26)

    font = ImageFont.truetype("Text_Style/DejaVuSansMono.ttf", size=10 * opt.scale)     ####### TEXT STYLE
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)        
        num_rows = int(height / cell_height)
    char_width, char_height = font.getsize("A")       
    out_width = char_width * num_cols
    out_height = 2 * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):                      ############### DRAW THE IMAGE ##############################
        for j in range(num_cols):
            partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                            int(j * cell_width):min(int((j + 1) * cell_width), width), :]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            char = CHAR_LIST[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

    if opt.background == "black":
        cropped_image = out_image.getbbox()
    elif opt.background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    elif opt.background == "gray":
        cropped_image = ImageOps.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(opt.output)


if __name__ == '__main__':
    filename=input("Enter Filename with path : ")
    newfilename=input("Enter new filename with path and extension : ")
    opt = get_args(filename,newfilename)
    main(opt)

    