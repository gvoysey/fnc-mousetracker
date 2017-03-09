import cv2
import numpy as np


def process_frame(frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(frame_hsv, lower_red, upper_red)
    lower_red1 = np.array([170, 50, 50])
    upper_red1 = np.array([180, 255, 255])
    mask1 = cv2.inRange(frame_hsv, lower_red1, upper_red1)
    mask = mask0 + mask1
    output_img = frame_hsv.copy()
    output_img[np.where(mask == 0)] = 0
    output_grey = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(output_grey, 15, 255,
                                 cv2.THRESH_BINARY)
    # the value of 15 is chosen by trial-and-error to produce the best outline of the skull
    kernel = np.ones((5, 5), np.uint8)
    # square image kernel used for erosion
    erosion = cv2.erode(thresh1, kernel, iterations=1)
    # refines all edges in the binary image

    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE,
                               kernel)  # this is for further removing small noises and holes in the image

    image, contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = []  # list to hold all areas

    for contour in contours:
        ar = cv2.contourArea(contour)
        areas.append(ar)

    max_area = max(areas)
    max_area_index = areas.index(max_area)  # index of the list element with largest area

    cnt = contours[max_area_index]  # largest area contour
    return areas, closing


if __name__ == "__main__":
    frame = cv2.imread('first.png')
    areas, final = process_frame(frame)
    cv2.imshow('final', final)
