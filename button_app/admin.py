from django.contrib import admin
from .models import ClickCounter

@admin.register(ClickCounter)
class ClickCounterAdmin(admin.ModelAdmin):
    list_display = ['id', 'count', 'created_at', 'updated_at']
    list_display_links = ['id', 'count']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Основная информация', {
            'fields': ['count', 'created_at', 'updated_at']
        }),
    ]
    
    def has_add_permission(self, request):
        """Запрещаем создавать новые записи, только одна запись должна существовать"""
        if ClickCounter.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удалять запись"""
        return False
    
    actions = None  # Убираем действия массового редактирования