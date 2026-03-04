from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Thinker, Work, Quote
from .forms import QuoteForm, ThinkerForm
from.owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class Main(View):

    template = "content/thinkers.html"

    def get(self, request):
        q = request.GET.get("q") if request.GET.get("q") != None else ""
        quotes = Quote.objects.filter(
            Q(thinker__name__icontains=q)|
            Q(quote__icontains=q) |
            Q(created_by__username__icontains=q)) 
        
        context = {"quotes":quotes}
        return render(request, self.template, context)
    
class QuoteDetail(View):

    template = "content/quote.html"

    def get(self, request, pk):
        quote = Quote.objects.get(pk=pk)

        next_quote = Quote.objects.filter(pk__gt=quote.pk).order_by("pk").first()
        prev_quote = Quote.objects.filter(pk__lt=quote.pk).order_by("-pk").first()

        if not next_quote:
            next_quote = Quote.objects.order_by("pk").first()

        if not prev_quote:
            prev_quote = Quote.objects.order_by("-pk").first()
            
        context = {"quote":quote,
                   "next_quote": next_quote,
                   "prev_quote": prev_quote}
        
        return render (request, self.template, context)
    
    @method_decorator(login_required)
    def post(self, request, pk):

        quote = get_object_or_404(Quote, pk=pk)
        liked = quote.likes.filter(id=request.user.id).exists()

        if liked:
            quote.likes.remove(request.user)
        else:
            quote.likes.add(request.user)
        
        return redirect("content:quote", pk=pk)

        
    
class QuoteAdd(OwnerCreateView):

    template_name = "content/add_quote.html"
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy("content:main")

"""    def get(self, request):
        form = QuoteForm()
        context = {"form":form}
        return render (request, self.template, context)
    
    def post (self, request):
        form = QuoteForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("content:main")
        context = {"form": form}
        return render(request, self.template, context)"""

class QuoteEdit(OwnerUpdateView):

    template_name = "content/edit_quote.html"
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy("content:main")

class QuoteDelete(OwnerDeleteView):

    template_name = "content/delete_quote.html"
    model = Quote
    success_url = reverse_lazy("content:main")
    
class ThinkerAdd(LoginRequiredMixin, View):

    template = "content/add_thinker.html"

    def get(self, request):
        form = ThinkerForm()
        context = {"form":form}
        return render (request, self.template, context)
    
    def post (self, request):
        form = ThinkerForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect("content:addquote")
        #context = {"form": form}
        #return render(request, self.template, context)

class ThinkerEdit(OwnerUpdateView):

    template_name = "content/edit_thinker.html"
    model = Thinker
    form_class = ThinkerForm
    success_url = reverse_lazy("base:profile")

class ThinkerDelete(OwnerDeleteView):

    template_name = "content/delete_thinker.html"
    model = Thinker
    success_url = reverse_lazy("base:profile")