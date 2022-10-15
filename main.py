import cv2
import numpy as np
from PIL import Image
import pytesseract as ts
from pdf2image import convert_from_path
import csv
from multiprocessing import Pool

pages = convert_from_path('/tmp/ac125274.pdf', 500)

def chop_image(image, page_no):
    '''
    Chop image into rows and columns
    '''
    width, height = image.size
    image = np.asarray(image)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    image_number = 0
    min_area = 10000
    tuples = []
    for c in reversed(cnts):
        area = cv2.contourArea(c)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
            new_image = Image.fromarray(original[y:y+h, x:x+w])
            image_number += 1

            width, height = new_image.size
            if width > 3000:
                columns = 3
            elif width > 1500:
                columns = 2
            else:
                columns = 1
            piece_width = width / columns
            piece_height = height
            for column in range(columns):
                box = (
                    column * piece_width,
                    0,
                    (column + 1) * piece_width,
                    piece_height
                )
                cut = Image.fromarray(cv2.resize(np.asarray(new_image.crop(box).crop(
                    (16, 84, 917, 478))), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
                cut.save('cuts/{}_{}_{}.png'.format(page_no, image_number, column))

                # epic = cv2.resize(np.asarray(new_image.crop(box).crop((900, 10, 1250, 97))), None, fx=2, fy=1, interpolation=cv2.INTER_AREA)
                # for i in range(len(epic)):
                #     for j in range(len(epic[i])):
                #         if sum(epic[i][j]) > 300:
                #             epic[i][j] = [255, 255, 255]
                # epic = Image.fromarray(np.asarray(epic))
                # epic.save('epics/{}_{}_{}.png'.format(page_no, image_number, column))

                # deleted = np.asarray(cut).copy()
                dw, dh = cut.size
                deleted = cv2.threshold(np.asarray(cut), 20, 255, cv2.THRESH_BINARY_INV)[1]
                rotationMatrix = cv2.getRotationMatrix2D((dw / 2, dh / 2), -25, 1)
                deleted = cv2.warpAffine(deleted, rotationMatrix, (dw, dh))
                deleted = Image.fromarray(deleted)
                deleted.save(
                    'deleted/{}_{}_{}.png'.format(page_no, image_number, column))
                deleted_text = ts.image_to_string(deleted, config="-c tessedit_char_whitelist=delt --psm 1")
                if 'deleted' in deleted_text.lower():
                    print('Deleted', (image_number, column))
                    continue

                text = ts.image_to_string(cut, lang='tam+eng')
                # epic_text = ts.image_to_string(epic, lang='eng', config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -c tosp_min_sane_kn_sp=0 --psm 8")
                print('Done', (page_no, image_number, column))
                tuples.append((page_no, image_number, column, text))
    return tuples


def main():
    with Pool(4) as p:
        texts = p.starmap(chop_image, [(pages[i], i + 1) for i in range(2, len(pages) - 1)])
        with open('output.csv', 'w') as f:
            csvwriter = csv.writer(f)
            for text in texts:
                csvwriter.writerows(text)

main()
