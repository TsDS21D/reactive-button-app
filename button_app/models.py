from django.db import models

class ClickCounter(models.Model):
    count = models.IntegerField(default=0, verbose_name="Текущее значение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Счетчик нажатий"
        verbose_name_plural = "Счетчик нажатий"

    def __str__(self):
        return f"Счетчик: {self.count}"

    @classmethod
    def get_singleton(cls):
        """Возвращает единственный экземпляр счетчика"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj