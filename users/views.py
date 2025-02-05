from django.contrib.auth.views import LoginView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import LoginUserForm, RegisterUserForm, VerifForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('event:home')


class Registrtion_View(FormView):
    form_class = RegisterUserForm
    template_name = 'registration.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        verification_code = random.randint(100000, 999999)
        self.request.session['verification_code'] = verification_code
        self.request.session['registration_data'] = form.cleaned_data
        try:
            send_mail(
                "Подтверждение email",
                f"Ваш код подтверждения: {
                    verification_code} \n Если сообщение пришло по ошибке просто проигнорируйте его.",
                settings.EMAIL_HOST_USER,
                [email]
            )
            return redirect('users:verify_email')
        except:
            messages.error(
                self.request, "Некорректная почта. Пожалуйста, попробуйте снова.")
            return redirect('users:registration')


class Verify_email(FormView):
    form_class = VerifForm
    template_name = 'verif.html'

    def form_valid(self, form):
        entered_code = form.cleaned_data.get('number')

        verification_code = self.request.session.get('verification_code')

        if entered_code == str(verification_code):
            messages.success(
                self.request, "Почта успешно подтверждена, вы зарегистрированы.")
            registration_data = self.request.session.get('registration_data')

            user = User.objects.create_user(
                username=registration_data['username'],
                email=registration_data['email'],
                password=registration_data['password1'],
            )
            return redirect('users:login')
        else:
            messages.error(
                self.request, "Неверный код подтверждения. Пожалуйста, попробуйте снова.")
            return redirect('users:verify_email')

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, введите корректный код.")
        return self.render_to_response(self.get_context_data(form=form))
