import cv2
import numpy as np

fly = cv2.imread('fly64.png')

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    print('Press "q" to END')

while True:
    ret, frame = capture.read()
    if not ret:
        print('Problem with capture')
        break

    #Преобразуем frame в чб формат
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 11)
    ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
    
    #Для задания п.3 требуется разделить frame на левую и правую сторону: разделим линией
    height, width = frame.shape[:2]
    right_half_start = width // 2
    right_half_end = width
    
    #В качестве маркера я выбрала круг, найдем его
    marker = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30, minRadius = 1, maxRadius = 100)
    if marker is not None:
        marker = np.uint16(np.around(marker))
        # Берем макс. обнаруженный круг
        max_marker = max(marker[0, :], key=lambda x: x[2])
        (x, y, r) = max_marker
        
        #Изменяем размеры мухи в соот. с радиусом круга
        size_fly = r * 2 
        resized_fly = cv2.resize(fly, (size_fly, size_fly))

        #Опр координаты мухи
        y1, y2 = y - r, y + r
        x1, x2 = x - r, x + r
        if y1 >= 0 and y2 <= frame.shape[0] and x1 >= 0 and x2 <= frame.shape[1]:
            frame[y1:y2, x1:x2] = resized_fly  
            
        # Проверяем положение центра круга
        if right_half_start <= x <= right_half_end:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        # Отрисовываем центр круга и окружность
        cv2.line(frame, (right_half_start, 0), (right_half_start, height), color, 2)
        cv2.circle(frame, (x, y), 5, color, -1)
        cv2.circle(frame, (x, y), r, color, 3)
        
    cv2.imshow('Marker Tracking + fly', frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
