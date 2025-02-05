from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import EmailMessage
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView


from event_search.forms import AddPostForm, SupportForm
from API.get_my_responce import searh_place_with_responce_gpt
from .models import Event, Place, Upload_files
from django.contrib.auth import get_user_model as Person
import os


class IndexTemplate(TemplateView):
    template_name = 'index.html'


class FAQ_Template(TemplateView):
    template_name = 'FAQ.html'


class My_events_Template(ListView):
    template_name = 'my_events.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        return Event.objects.select_related('place', 'person').filter(person__username=self.request.user)


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_person.html'
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_event'

    def get_template_names(self):
        return [self.template_name]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event.place.delete()
        return redirect('event:my_events')


class Create_event(FormView):
    form_class = AddPostForm
    template_name = 'create_event.html'
    template_error = 'errors.html'
    success_url = reverse_lazy('my_events')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        content = searh_place_with_responce_gpt(
            cleaned_data['name'], cleaned_data['place'], cleaned_data['wish']
        )
        if 'text' not in content:
            event = content['event']
            rating_str = event['rating'].replace(',', '.')
            try:
                place = Place(
                    name=event['place'],
                    image_url=event['image'],
                    website=event['Url'],
                    rating=float(rating_str),
                    city=cleaned_data['place']
                )
                if self.request.user.is_authenticated:
                    event_obj = Event(
                        name=content['event_name'],
                        plan=content['response_gpt'],
                        person=Person().objects.get(username=self.request.user),
                        place=place
                    )
                    place.save()
                    event_obj.save()
                    return redirect('event:my_events')
                else:
                    event_obj = Event(
                        name=content['event_name'],
                        plan=content['response_gpt'],
                        place=place
                    )
                    return render(self.request, 'event_person.html', context={'event': event_obj})
            except Exception as e:
                return render(self.request, 'errors.html', context={
                    'text': 'Ошибка создания мероприятия',
                    'result': f"Возникла ошибка: {str(e)}, обратитесь в поддержку."
                })
        return render(self.request, 'errors.html', context=content)

    def form_invalid(self, form):
        error_messages = ""
        for field in form:
            for error in field.errors:
                error_messages += f"{field.label}: {error}\n"

        error_messages = (error_messages
                          .replace('Name', 'Название мероприятия')
                          .replace('Place', 'Место проведения')
                          .replace('Wish', 'Пожелания')
                          .replace('Agree', 'Согласие')
                          )

        return render(self.request, self.template_error, {
            'text': 'Форма не валидна',
            'result': error_messages
        })


class SupportForm(FormView):
    form_class = SupportForm
    template_name = 'support.html'
    template_error = 'errors.html'

    def form_valid(self, form):
        form = form.cleaned_data
        email = EmailMessage(
            subject=f'Обращение пользователя: {form["name"]}',
            body=f'Спасибо за обращение {
                form["name"]}, наши специалисты начали решать вашу проблему.\n Если это письмо попало к вам по ошибке, пожалуйста, проигнорируйте его. \n'
            f'Ваше обращение:\n {form["text"]}',
            from_email=settings.EMAIL_HOST_USER,
            to=[form['mail'], settings.EMAIL_HOST_USER]
        )
        if form['image']:
            fp = Upload_files(file=form['image'])
            fp.save()
            email.attach_file(fp.file.path)
            file_path = fp.file.path
            os.remove(file_path)
            fp.delete()
        email.send()
        return render(self.request, 'errors.html', context={'text': 'Спасибо за обращения', 'result': 'Ваще соообщение зарегистрировано, ожидайте ответ на указанную вами почту.'})

    def form_invalid(self, form):
        error_messages = ""
        for field in form:
            for error in field.errors:
                error_messages += f"{field.label}: {error}\n"

        error_messages = (error_messages
                          .replace('Name', 'Имя')
                          .replace('Mail', 'Почта')
                          .replace('Text', 'Текст вопроса')
                          )
        return render(self.request, self.template_error, {
            'text': 'Форма не валидна',
            'result': error_messages
        })


class EventDelete(DeleteView):
    model = Place
    success_url = reverse_lazy('my_events')


def pagenotfound(request, exception):
    return render(request, 'errors.html', context={'text': "Страница не найдена", 'result': "Извините, но мы не смогли найти эту страницу. Пожалуйста, проверьте URL или вернитесь на главную страницу."})


def server_is_not_good(request, exception):
    return render(request, 'errors.html', context={'text': "Страница временна не доступна", 'result': "Извините, возникла критическая ошибка на стороне сервера, наши разработчики уже этим занимаются."})


def server_is_500(request):
    return render(
        request,
        'errors.html',
        context={
            'text': "Страница временно недоступна",
            'result': f"Возникла ошибка на стороне сервера. Если ошибка сохраняется, обратитесь в поддержку, указав код ошибки 500."
        }
    )
