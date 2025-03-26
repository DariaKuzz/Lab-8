import cv2

img = cv2.imread('variant-4.jpeg')

# Разделим цветовые каналы изображения
b, g, r = cv2.split(img) 
if __name__ == "__main__":
    cv2.imshow('img', img)
    cv2.imshow('blue', b)

cv2.waitKey(0)
cv2.destroyAllWindows()
