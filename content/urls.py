from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("", views.Main.as_view(), name="main"),
    path("quote/<int:pk>/", views.QuoteDetail.as_view(), name="quote"),
    path("add_quote/", views.QuoteAdd.as_view(), name="addquote"),
    path("edit_quote/<int:pk>/", views.QuoteEdit.as_view(), name="editquote"),
    path("delete_quote/<int:pk>/", views.QuoteDelete.as_view(), name="deletequote"),
    path("add_thinker/", views.ThinkerAdd.as_view(), name="addthinker"),
    path("edit_thinker/<int:pk>/", views.ThinkerEdit.as_view(), name="editthinker"),
    path("delete_thinker/<int:pk>/", views.ThinkerDelete.as_view(), name="deletethinker")
    ]
