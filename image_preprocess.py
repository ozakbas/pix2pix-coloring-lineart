from PIL import Image, ImageFilter, ImageOps
from os import listdir, rename, mkdir
from numpy import asarray


main_path = "C:/Users/ereno/Desktop/pix2pix_data" + "/"
input_path = "C:/Users/ereno/Desktop/pix2pix_data/input" + "/"
ss_path = main_path + "4_1/"
height = 1920
width = 1080
target = 256 # target image size 256x256

def rename_images(path):

    for i, filename in enumerate(listdir(path)):
        rename(path + filename, path + str(i) + ".png")


def calculate_remainders(height, width, target):

    remainder_right = height % target
    remainder_bottom = width % target

    return remainder_right, remainder_bottom


#crop images to achieve multiples of 256
def crop_images(ss_path):

    r1, r2 = calculate_remainders(height, width, target)
    mkdir(main_path + "cropped")

    for i, filename in enumerate(listdir(ss_path)):
        img = Image.open(ss_path + filename)
        img1 = img.crop((0, 0, height - r1, width - r2))
        img1.save(main_path + "cropped/" + str(i) + ".png")


def split_images():

    cropped_path = main_path + "cropped/"
    mkdir(main_path + "splitted")

    count = 0
    for filename in listdir(ss_path):
        im = Image.open(cropped_path + filename)
        im = asarray(im)

        tiles = [im[x:x+target,y:y+target] for x in range(0,im.shape[0],target) for y in range(0,im.shape[1],target)]

        for tile in tiles:
            img = Image.fromarray(tile)
            img.save(main_path + "splitted/" + str(count) + ".png")
            count += 1


def merge_images(input_path, splitted_path, n_images):

    mkdir(main_path + "merged")

    for i in range(n_images):
        im1 = Image.open(splitted_path + "/{}.png".format(i))
        im2 = Image.open(input_path + "/{}.png".format(i))

        img = Image.new('RGB', (im1.width + im2.width, im1.height))
        img.paste(im1, (0, 0))
        img.paste(im2, (im1.width, 0))

        img.save(main_path + "merged2/" + str(i) + ".png")



def decolor_images():

    mkdir(main_path + "decolored2")

    for i in range(4057):
        image = Image.open(main_path + "splitted/"+ str(i) + ".png")

        image = image.convert("L")
        image = image.filter(ImageFilter.FIND_EDGES)
        image = ImageOps.invert(image)
        
        image.save(main_path + "decolored2/" + str(i) + ".png")



#rename_images(input_path)
#crop_images(ss_path)
#split_images()
#decolor_images()
#merge_images(main_path + "decolored", main_path + "splitted", 4057)

