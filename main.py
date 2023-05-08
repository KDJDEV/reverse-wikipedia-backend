#processes images and adds them to database

from zimplyIterate import ZIMIterator
from imageProcessor import imageProcessor
imageProcessorObject = imageProcessor()

startAtIndex = 0
endAtIndex = 16519000 #this is only used for the percent completed and so does not need to be perfectly accurate

def processImage(imageBinary, url):
    imageProcessorObject.processImage(imageBinary, url)

server = ZIMIterator("wikipedia_en_all_maxi_2022-05.zim", callback=processImage, startAtIndex=startAtIndex, endAtIndex=endAtIndex)