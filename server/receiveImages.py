import ftplib
import io
import os

import cv2 as cv2
import numpy as np

session = ftplib.FTP('192.168.1.59', 'pucci', 'pi')
# filename = 'frame0.jpg'
# file = open('./../image.jpg', 'rb')
# for file in os.listdir('frames'):
# ftpResponse = session.storbinary(f'STOR image.jpg', file)
# print(ftpResponse)
# file.close()
session.dir()
print('-------------------------------------')
# ftpResponse = session.delete('frame0.jpg')
# print(ftpResponse)
# session.dir()
dir = '../resources/frames/'

for file in os.listdir(dir):
    r = io.BytesIO()
    print(file)
    ftpResponse = session.retrbinary('RETR ' + str(file), r.write)
    print(ftpResponse)
    image = np.asarray(bytearray(r.getvalue()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite("./../output/" + str(file), image)
session.quit()

