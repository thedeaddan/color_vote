[app]

# (строка) Имя Вашего приложения
title = Color Vote

# (строка) Пакет (идентификатор приложения)
package.name = colorvote
package.domain = org.thedeaddan

# (строка) Версия вашего приложения
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# (строка) Путь к исходным файлам приложения
source.dir = .

# (список) Используемые библиотеки (должны быть установлены через pip)
requirements = python3,kivy,plyer,requests

# (строка) Настройки для Android
android.permissions = CAMERA
android.api = 27
android.ndk = 21.1.6352462
android.arch = arm64-v8a
