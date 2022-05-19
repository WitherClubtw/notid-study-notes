# Compress png files to jpg, then coverts them to pdf.
#
# This is a disgusting workaround for the fact that I didn't read tne docs
# But the exam is in 2 days, so this is as good as it gets
# =============================================================================
# Instructions:
# Put this file in the same directory as the images and run it.
import os
from PIL import Image
import datetime
from fpdf import FPDF


# Thank the all-mighty copilot for saving me 30 minutes of my life
def fillPageScaling(paperWidth, paperHeight, imageWidth, imageHeight):
    paperRatio = paperWidth / paperHeight
    imageRatio = imageWidth / imageHeight

    if paperRatio > imageRatio:
        # image is too tall
        # scale it to fit the paper height
        return paperHeight * imageRatio, paperHeight
    else:
        # image is too wide or perfect fit
        # scale it to fit the paper width
        return paperWidth, paperWidth / imageRatio


dirname = os.path.dirname(__file__)

fileList = [i for i in os.listdir(dirname) if i.endswith('.png')]
fileList.sort()

# Convert all images to jpg
print("============ Compressing images to jpg ============")
jpgDirname = os.path.join(dirname, 'jpg/')
if not os.path.exists(jpgDirname):
    os.makedirs(jpgDirname)

jpgList = []
for i in fileList:
    startTime = datetime.datetime.now()

    im = Image.open(os.path.join(dirname, i))
    rgb_im = im.convert('RGB')

    path = os.path.join(jpgDirname, i.replace('.png', '.jpg'))
    rgb_im.save(path, optimize=True, quality=30)

    jpgList.append(path)
    print("Processing:", i, "Elapsed Time:", datetime.datetime.now() - startTime)

# Convert all images to pdf
print("============ Converting jpg to pdf ============")
output = FPDF("P", "mm", "A4")
for i in jpgList:
    startTime = datetime.datetime.now()

    f = Image.open(i)
    width, height = f.size
    newWidth, newHeight = fillPageScaling(210, 297, width, height)

    output.add_page()
    output.image(i, 0, 0, newWidth, newHeight)

    print("Processing:", os.path.basename(i), "Elapsed Time:", datetime.datetime.now() - startTime)

output.output(os.path.join(dirname, "output.pdf"), "F")
