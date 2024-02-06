import cv2
import numpy as np
import time
import webcolors

def calibrate_background(cap):
    print("Калибровка фона. Подготовьтесь...")
    time.sleep(1)
    
    background_frames = []
    for _ in range(5):
        ret, frame = cap.read()
        if not ret:
            print("Ошибка при получении кадра.")
            return None
        
        background_frames.append(frame)
        time.sleep(1)

    background = np.median(np.array(background_frames), axis=0).astype(np.uint8)
    return background

def find_colored_rectangles(frame, background, color_ranges, ignore_colors):
    diff = cv2.absdiff(frame, background)
    diff_hsv = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)
    
    colored_rectangles = []
    
    for color_range in color_ranges:
        lower_color = np.array(color_range[0])
        upper_color = np.array(color_range[1])
        
        mask = cv2.inRange(diff_hsv, lower_color, upper_color)
        _, threshold = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                roi = frame[y:y+h, x:x+w]
                
                # Проверка на игнорируемые цвета
                ignore_color = np.median(np.median(roi, axis=0), axis=0).astype(np.uint8)
                if any(np.all(ignore_color == ic) for ic in ignore_colors):
                    continue
                
                color = np.median(np.median(roi, axis=0), axis=0).astype(np.uint8)
                color_name = get_color_name(color)
                
                colored_rectangles.append(((x, y, w, h), roi, color_name))
    
    return colored_rectangles

def get_color_name(rgb_color):
    try:
        color_name = webcolors.rgb_to_name(rgb_color)
    except ValueError:
        color_name = f"RGB({rgb_color[0]}, {rgb_color[1]}, {rgb_color[2]})"
    return color_name

def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка при открытии камеры.")
        return
    
    background = calibrate_background(cap)
    
    if background is None:
        print("Ошибка калибровки фона.")
        cap.release()
        return
    
    print("Калибровка завершена. Начало отслеживания прямоугольников.")
    
    color_ranges = [([0, 120, 70], [10, 255, 255]),  # Диапазон красного
                    ([40, 40, 40], [80, 255, 255])]  # Диапазон зеленого
    
    ignore_colors = [[89, 106, 184]]  # Цвет для игнорирования

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка при получении кадра.")
            break

        colored_rectangles = find_colored_rectangles(frame, background, color_ranges, ignore_colors)

        for (x, y, w, h), roi, color_name in colored_rectangles:
            cv2.putText(frame, f'Цвет: {color_name}', (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), roi.mean(axis=(0, 1)).astype(int).tolist(), 2)

        cv2.imshow('Colored Rectangles Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
