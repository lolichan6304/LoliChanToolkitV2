import numpy as np
import cv2

def rgb_to_hsv(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

def hsv_to_rgb(im):
    return cv2.cvtColor(im, cv2.COLOR_HSV2BGR)

"""image = "pic_003.jpg"

edges = cv2.imread("canny_fix.jpg", 0)
img = cv2.imread(image)
for i in range(len(img)):
    for j in range(len(img[i])):
        if edges[i][j] <= 50 and edges[i][j] != 0:
            print(edges[i][j])
            edges[i][j] = 0
        elif edges[i][j] >= 200 and edges[i][j] != 255:
            print(edges[i][j])
            edges[i][j] = 255
cv2.imwrite("canny_fix.jpg", edges)
edges = cv2.imread("canny_fix.jpg", 0)
for i in range(len(img)):
    for j in range(len(img[i])):
        if edges[i][j] == 0:
            img[i,j,:] = 255*np.ones_like(img[i,j,:])
cv2.imwrite("canny_color.jpg", img)"""

image = "pic_{:03d}.jpg"
edges = cv2.imread("canny_fix.jpg", 0)
edges_2 = cv2.imread("canny_color.jpg")*1.
# reverse the alpha
alpha = 0.3
mask = 255*np.ones_like(edges_2)
true_ = (edges_2 - (1-alpha)*mask)/alpha
for i in range(1,35):
    io = cv2.imread(image.format(i))
    result = (io - alpha*true_)/(1-alpha)
    #mask = 255*np.ones_like(edges_2)
    #result = (io + (mask - edges_2))
    #result = cv2.inpaint(io, edges, 50, cv2.INPAINT_TELEA)
    cv2.imwrite("result_{:03d}.jpg".format(i), result)

"""img = cv2.imread(image, 0)

for i in range(len(img)):
    for j in range(len(img[i])):
        if i <= 1000 or i >= 2000:
            img[i][j] = 255
        else:
            if img[i][j] < 220:
                img[i][j] = 0
cv2.imwrite("preprocess.jpg", img)

edges = cv2.Canny(img,100,200)"""
"""th, edges = cv2.threshold(edges, 1, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("canny_temp.jpg", edges)
edges_floodfill = edges.copy()
h, w = edges.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
cv2.floodFill(edges_floodfill, mask, (0,0), 255)
for i in range(len(edges_floodfill)):
    for j in range(len(edges_floodfill[i])):
        if edges_floodfill[i][j] == 120:
            edges_floodfill[i][j] == 255
        else:
            edges_floodfill[i][j] == 0
edges = edges | edges_floodfill"""

"""cv2.imwrite("canny.jpg", edges)"""




"""fill_in_method = cv2.INPAINT_TELEA
io_hsv        = rgb_to_hsv(io)
h_before      = io_hsv[:,:,0]
s_before      = io_hsv[:,:,1]
v_before      = io_hsv[:,:,2]

#outer_mask_uint    = np.where(outer_mask,255,0).astype(np.uint8)
#s_after   = cv2.inpaint(s_before, outer_mask_uint, 15, fill_in_method)       # use outer mask to fill in saturation
#h_after   = cv2.inpaint(h_before, outer_mask_uint, 15 ,fill_in_method)       # use outer mask to fill in hue
v_after   = cv2.inpaint(v_before,       edges,  2, fill_in_method)  # use edge to fill in hue"""

"""io_hsv[:,:,0] = h_before
io_hsv[:,:,1] = s_before
io_hsv[:,:,2] = v_after
cv2.imwrite("result.jpg", hsv_to_rgb(io_hsv))"""


print(edges)

