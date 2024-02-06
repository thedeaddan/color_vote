from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import requests
from PIL import Image

class ColorSquare(BoxLayout):
    def __init__(self, **kwargs):
        super(ColorSquare, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = 100
        self.height = 100
        self.color = Color(1, 1, 1, 1)  # Белый цвет по умолчанию
        self.canvas.add(self.color)
        self.canvas.add(Rectangle(pos=self.pos, size=self.size))

    def update_color(self, new_color):
        self.color.rgb = [val / 255.0 for val in new_color]

class CameraApp(App):
    def build(self):
        self.camera = Camera(index=0, resolution=(1080, 1920), play=True)
        self.img_texture = None

        layout = BoxLayout(orientation='vertical')

        self.color_square = ColorSquare()
        layout.add_widget(self.camera)
        layout.add_widget(self.color_square)

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Обновление img_texture каждые 1/30 секунды
        Clock.schedule_interval(self.automatic_scan, 5.0)  # Автоматическое сканирование каждые 5 секунд

        return layout

    def update(self, dt):
        if self.camera.texture:
            self.img_texture = self.camera.texture

    def scan_color(self):
        if self.img_texture:
            # Получаем данные о цвете кружочка (в данном случае, центр изображения)
            img = Image.frombytes('RGBA', (self.img_texture.width, self.img_texture.height), self.img_texture.pixels)
            center_pixel = img.getpixel((self.img_texture.width // 2, self.img_texture.height // 2))

            # Преобразуем цвет в формат RGB
            color = center_pixel[:3]

            # Обновляем цвет квадрата
            self.color_square.update_color(color)

            # Отправляем данные на сервер
            #self.send_to_server(color)    

    def automatic_scan(self, dt):
        self.scan_color()  # Вызываем функцию сканирования

    def send_to_server(self, color):
        # Настройте ваш API-URL и параметры запроса
        api_url = "https://example.com/api/scan"
        headers = {'Content-Type': 'application/json'}
        payload = {'color': color}

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                print("Данные успешно отправлены на сервер.")
            else:
                print(f"Ошибка при отправке данных. Код ответа: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")

if __name__ == '__main__':
    CameraApp().run()
