import pytesseract
import pyautogui
from PIL import Image

# FOR WINDOWS:
# pytesseract.pytesseract.tesseract_cmd = PATH_TO_TESSERACT

region = (0, 0, 1920, 1080)
sentence = "Hello"

def find_sentence(sentence, region, take_screenshot, moveMouse):

    screenshot_name = take_screenshot(*region)
    image = Image.open(PATH + screenshot_name)
    
    gray = image.convert('L')
    
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    words = sentence.split()
    
    indices = []
    for word in words:
        try:
            index = data['text'].index(word)
            indices.append(index)
        except ValueError:
            pass
    
    if indices:

        x1s = [data['left'][index] for index in indices]
        y1s = [data['top'][index] for index in indices]

        x1 = min(x1s)
        y1 = max(y1s)
        x2 = max(x1s)
        y2 = max(y1s)
    
    x_center = (x1 + x2) // 2
    y_center = (y1 + y2) // 2
    
    x_center += region[0]
    y_center += region[1]

    moveMouse(x_center, y_center)
        
    return (x1, y1), (x2, y2)


def take_screenshot(x, y, width, height):
    filename = 'screenshot.png'
    pyautogui.screenshot(filename, region=region)

    return filename

def moveMouse(x, y):
    pyautogui.moveTo(x, y)
    pass

def main():

    coordinates = find_sentence(sentence, region, take_screenshot, moveMouse)

    if coordinates:
        print(f"The sentence '{sentence}' was found at coordinates {coordinates}.")
    else:
        print(f"The sentence '{sentence}' was not found in the specified region of the screen.")


if __name__ == '__main__':
    main()