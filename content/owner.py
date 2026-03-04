from django.views.generic import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super(UpdateView, self).get_queryset()
        return qs.filter(created_by=self.request.user)
    
class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super(DeleteView, self).get_queryset()
        return qs.filter(created_by=self.request.user)