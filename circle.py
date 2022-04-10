import cv2
import sys
import numpy as np

def kernel(n):
	n = int(n/2)
	y,x = np.ogrid[-n: n+1, -n: n+1]
	mask = x**2+y**2 <= n**2
	array = np.zeros((2*n+1, 2*n+1), dtype=np.uint8)
	array[mask] = 255
	print(array)
	print(array.dtype)
	return array

	#return np.ones((n,n))

filename1 = sys.argv[1]
filename2 = sys.argv[2]
outfilename = sys.argv[3]

img1 = cv2.imread(filename1)
img2 = cv2.imread(filename2)

print("HASS")

ret, mask0 = cv2.threshold(np.abs(img1 - img2), 0.1, 1000, cv2.THRESH_BINARY)
mask0 = cv2.cvtColor(mask0, cv2.COLOR_RGB2GRAY)
ret, mask0 = cv2.threshold(mask0, 0.1, 1000, cv2.THRESH_BINARY)

mask = cv2.dilate(cv2.erode(mask0, kernel(5)), kernel(5))
mask = cv2.erode(cv2.dilate(mask, kernel(200)), kernel(200))
mask = cv2.dilate(mask, kernel(100))

img2[mask0 == 0] //= 3
img2[mask0 == 0] += (192 - 128//3)


contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for c in contours:
	e = cv2.fitEllipse(c)
	print(e)
	cv2.ellipse(img2, e, (0,0,255), 5)


cv2.imwrite(outfilename, img2)

#cv2.imshow("mask", img2)
#while True:
#	cv2.waitKey(100)

