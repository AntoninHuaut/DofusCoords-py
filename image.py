import cv2
import mss
import numpy

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC) # Scale image first (4x upscaling)   
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = numpy.ones((2, 2), numpy.uint8)  
    img = cv2.dilate(img, kernel, iterations=1)
    sharpen_kernel = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, sharpen_kernel)
    img = cv2.medianBlur(img, 3)
    img = cv2.bitwise_not(img)

    return img

def readtext(reader, image_path):
    result = reader.readtext(
        image_path,
        paragraph=True,
        min_size=20,
        # contrast_ths=0.3,
        text_threshold=0.35,  # Lower threshold for better number recognition
        # width_ths=2.0,  # Increased width threshold for connected digits
        mag_ratio=2.0  # Additional magnification
    )
    return result

def screenshot(sct, monitor, output_path):
    screenshot = sct.grab(monitor)
    mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)

def cleanCoordinate(data):
    coords = data.strip()
    similarChars =  ["−", "—", "–", "―", "~", "‒", "‑"]
    for c in similarChars:
        coords = coords.replace(c, "-")

    isNegative = coords[0] == "-"
    coords = ''.join(c for c in data if c in "0123456789")
    if isNegative:
        coords = "-" + coords
    return coords