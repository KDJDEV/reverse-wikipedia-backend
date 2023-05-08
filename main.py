#processes images and adds them to database

from zimplyIterate import ZIMIterator
from imageProcessorBinary import imageProcessor
imageProcessor = imageProcessor()

startAtIndex = 0 #16519000
endAtIndex = 16519000 #this is only used for the percent completed and so does not need to be perfectly accurate

def processImage(imageBinary, url):
    imageProcessor.processImage(imageBinary, url)

server = ZIMIterator("wikipedia_en_all_maxi_2022-05.zim", callback=processImage, startAtIndex=startAtIndex, endAtIndex=endAtIndex)