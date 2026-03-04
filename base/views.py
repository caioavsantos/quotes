from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from content.models import Thinker, Quote
from django.contrib.auth.mixins import LoginRequiredMixin
from content.service import get_day_quote
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit


class Homepage(View):

    template = "base/home.html"

    def get(self, request):
        quote = get_day_quote()
        return render(request, self.template, {"quote":quote})


class LoginPage (View):

    template = "base/login_register.html"
    page = "login"

    def get(self, request):
        return render(request, self.template, {"page":self.page})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or "base:home"
            return redirect(next_url)
        
        messages.error(request, "Incorrect username or password")
        return render(request, self.template, {"page":self.page})

@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="dispatch")
@method_decorator(ratelimit(key="ip", rate="20/d", block=True), name="dispatch")    
class RegisterPage(View):

    template = "base/login_register.html"
    page = "register"

    def get(self, request):
        form = UserCreationForm()
        context = {"form": form,
                   "page":self.page}
        
        return render(request, self.template, context)
        
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            if user is not None:
                login (request, user)
            
            return redirect("base:home")
        
        else:
            messages.error(request, "Oops, something went wrong")
            return render(request, self.template, {"form": form, "page": self.page})


def logoutUser(request):
    logout(request)
    return redirect("base:home")

class Profile(LoginRequiredMixin, View):

    template = "base/profile.html"

    def get(self, request):
        thinkers = Thinker.objects.filter(created_by=request.user)
        quotes = Quote.objects.filter(created_by=request.user)
        likes = request.user.liked_quotes.all()
        context = {"thinkers": thinkers,
                   "quotes": quotes,
                   "likes": likes}
        return render (request, self.template, context)


class About(View):

    template = "base/about.html"

    def get(self, request):
        return render(request, self.template)
