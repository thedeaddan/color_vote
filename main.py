from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import requests

class CameraApp(App):
    def build(self):
        self.camera = Camera(resolution=(640, 480), play=True)
        self.capture = None
        self.img_texture = None

        layout = BoxLayout(orientation='vertical')

        self.btn_scan = Button(text='Scan Color', on_press=self.scan_color)
        layout.add_widget(self.camera)
        layout.add_widget(self.btn_scan)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return layout

    def update(self, dt):
        if self.camera.texture:
            self.img_texture = self.camera.texture

    def scan_color(self, instance):
        if self.img_texture:
            # Считываем цвет кружочка (в данном случае, центр изображения)
            center_pixel = self.img_texture.pixels[(self.img_texture.width // 2, self.img_texture.height // 2) * 3:][:3]
            
            # Преобразуем цвет в формат RGB
            color = [int(val * 255) for val in center_pixel]

            # Отправляем данные на сервер
            self.send_to_server(color)

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
