import numpy as np
from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
import matplotlib.pyplot as plt

def draw_grid(img_path: str,output_path: str, gridSize: int):
    img = Image.open(img_path)
    img_draw = ImageDraw.Draw(img)
    write = ImageDraw.Draw(img)
    ct = ColorThief(img_path)

    # get the dominant color and display it
    dominantColor = ct.get_color(quality=1)
    # plt.imshow([dominantColor])
    # plt.show()

    # get the contrasting color and display it
    contrast = []
    for i in dominantColor:
        contrast.append(255-i)
    # plt.imshow([contrast])
    # plt.show()
    contrast_color = tuple(contrast)

    width, height = img.size
    font_size = int(gridSize*0.2)
    font = ImageFont.truetype("arial/arial.ttf", font_size)

    pos =1
    for x in range(0, width, gridSize):
        img_draw.line((x,0,x, height),fill=contrast_color, width=2)
        write.text((x + 15, 20), str(pos), font=font, fill=contrast_color)
        pos+=1
    pos = 0
    for y in range(0, height, gridSize):
        pos+=1
        img_draw.line((0,y, width, y), fill=contrast_color, width=2)
        if pos == 1:
            continue
        write.text((20, y + 15), str(pos), font=font, fill=contrast_color)

    img.save(output_path)
    return output_path
def getSize(img_path:str):
    img = Image.open(img_path)
    return img.size


if __name__ == '__main__':
    draw_grid("photos/g20.jpeg", "sample3.jpeg", 50)
    print(getSize("photos/g20.jpeg"))