import py_compile
import numpy
import sys
import cv2

from src.slic import *

# python testslic.py test.png 500 40
img = cv2.imread(sys.argv[1])

step = int((img.shape[0]*img.shape[1]/int(sys.argv[2]))**0.5)
SLIC_m = int(sys.argv[3])
SLIC_ITERATIONS = 4
SLIC_height, SLIC_width = img.shape[:2]
SLIC_labimg = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(numpy.float64)
SLIC_distances = 1 * numpy.ones(img.shape[:2])
SLIC_clusters = -1 * SLIC_distances
SLIC_center_counts = numpy.zeros(len(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg)))
SLIC_centers = numpy.array(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg))

# main
generate_pixels(img,SLIC_height,SLIC_width,SLIC_ITERATIONS,SLIC_centers,
                step,SLIC_labimg,SLIC_m,SLIC_clusters)
create_connectivity(img,SLIC_width,SLIC_height,SLIC_centers,SLIC_clusters)
display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0.0, 0.0, 0.0])
cv2.imshow("superpixels", img)
cv2.waitKey(0)
cv2.imwrite("500_40.jpg", img)