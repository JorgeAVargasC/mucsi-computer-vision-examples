import cv2

img = cv2.imread("./statue_small.jpg", 0)

cv2.imwrite("13_output_canny.jpg", cv2.Canny(img, 200, 300))
cv2.imshow("canny", cv2.imread("13_output_canny.jpg"))

cv2.waitKey()
cv2.destroyAllWindows()
