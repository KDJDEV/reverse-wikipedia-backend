import imagehash
from PIL import Image
import cairosvg
from io import BytesIO
def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im
def twos_complement(hexstr, bits):
        value = int(hexstr,16)
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value
def getHashInt(imageBinary, converted): #imageBinary is BytesIO object
    try:
        if isinstance(imageBinary, str): #if not BytesIO object
            with open(imageBinary, "rb") as image: #then assume it's a path to a file
                imageBinary = BytesIO(image.read())
        img = Image.open(imageBinary)
        img = remove_transparency(img)
        imgHash = str(imagehash.dhash(img))
        hashInt = twos_complement(imgHash, 64)
        return hashInt
    except:
        if (not converted):
            #it may be an svg
            buff = BytesIO()
            cairosvg.svg2png(bytestring=imageBinary.getvalue(), write_to=buff)
            buff.seek(0)

            return getHashInt(buff, True)
        else:
            raise Exception('Image processing error')
        