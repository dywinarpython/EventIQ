from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Event, Place, Upload_files


class RatingFillter(admin.SimpleListFilter):
    title = 'Фильтр рейтинга'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('high', 'Рейтинг больше 4.5'),
            ('low', 'Рейтинг меньше или равен 4.5')
        )

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(rating__gt=4.5)
        elif self.value() == 'low':
            return queryset.filter(rating__lte=4.5)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plan', 'time_create',
                    'person', 'place', 'slug')
    readonly_fields = ('slug', )
    list_display_links = ('id',)
    ordering = ['-time_create', 'name']
    list_editable = ('person', 'name', 'place')
    list_per_page = 10
    search_fields = ('name', )
    list_filter = ('time_create', )


# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('id', 'login', 'email')
#     list_display_links = ('id', 'login')
#     search_fields = ('login', )


@admin.register(Place)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_image', 'website', 'rating', 'city')
    list_display_links = ('id',)
    list_editable = ('name', 'rating', 'city')
    search_fields = ('name', 'city')
    list_filter = (RatingFillter, )

    @admin.display(description='Вид изображения', ordering='rating')
    def display_image(self, place: Place):
        if place.image_url:
            return mark_safe(f"<img src='{place.image_url}' width=50>")
        return 'Без фота'
    save_on_top = True


@admin.register(Upload_files)
class Upload_files_Admin(admin.ModelAdmin):
    list_display = ('file', )
    list_display_links = ('file', )
