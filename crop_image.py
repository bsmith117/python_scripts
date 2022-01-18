def crop_image(path,left,top,right,bottom,output_path):
    from PIL import Image

# Opens a image in RGB mode

    #path = r"/Users/Brandon/PycharmProjects/WaveApp/screenshot-headless.png"
    im = Image.open(path)

# Setting the points for cropped image
    #left = 10
    #top = 310
    #right = 600
    #bottom = 470

# Cropped image of above dimension
# (It will not change orginal image)
    im = im.crop((left, top, right, bottom))

# Shows the image in image viewer
    #im1.show()
    im = im.save(output_path)