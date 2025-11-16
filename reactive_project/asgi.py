"""
ASGI config for reactive_project project.
"""

import os
import django
from django.core.asgi import get_asgi_application

# Устанавливаем настройки Django ДО всех импортов
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reactive_project.settings')
django.setup()

# Теперь импортируем WebSocket компоненты
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from asgiref.sync import sync_to_async

# Импортируем модель
from button_app.models import ClickCounter

# WebSocket consumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ButtonConsumer(AsyncWebsocketConsumer):
    # Список активных подключений
    connections = []

    async def connect(self):
        print("🟢 WebSocket: Успешное подключение")
        # Добавляем соединение в список
        self.connections.append(self)
        await self.accept()
        
        # Получаем текущее значение счетчика из базы
        current_count = await self.get_current_count()
        
        # Отправляем текущее значение счетчика
        await self.send(json.dumps({
            'type': 'connection_established',
            'message': 'WebSocket подключен!',
            'count': current_count
        }))

    async def disconnect(self, close_code):
        print(f"🔴 WebSocket: Отключение (код: {close_code})")
        # Удаляем соединение из списка
        if self in self.connections:
            self.connections.remove(self)

    async def receive(self, text_data):
        print(f"📨 WebSocket: Получено сообщение - {text_data}")
        try:
            data = json.loads(text_data)
            
            if data.get('type') == 'button_click':
                # Увеличиваем счетчик в базе данных
                new_count = await self.increment_counter()
                print(f"🔘 Кнопка нажата! Текущее значение: {new_count}")
                
                # Рассылаем обновление всем подключенным клиентам
                message = json.dumps({
                    'type': 'count_update',
                    'count': new_count
                })
                
                # Создаем копию списка для безопасной итерации
                connections_copy = self.connections.copy()
                for connection in connections_copy:
                    try:
                        await connection.send(message)
                    except Exception as e:
                        print(f"⚠️ Ошибка отправки: {e}")
                        # Удаляем нерабочие соединения
                        if connection in self.connections:
                            self.connections.remove(connection)
                            
        except Exception as e:
            print(f"❌ Ошибка обработки сообщения: {e}")

    @sync_to_async
    def get_current_count(self):
        """Получает текущее значение счетчика из базы данных"""
        counter = ClickCounter.get_singleton()
        return counter.count

    @sync_to_async
    def increment_counter(self):
        """Увеличивает счетчик в базе данных и возвращает новое значение"""
        counter = ClickCounter.get_singleton()
        counter.count += 1
        counter.save()
        return counter.count

# WebSocket маршрутизация
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/button/", ButtonConsumer.as_asgi()),
        ])
    ),
})