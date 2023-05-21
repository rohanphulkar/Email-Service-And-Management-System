from django.urls import path
from .import views

urlpatterns = [
    path("",views.mails_table,name="home"),
    path("<id>/",views.mail,name="mail"),
    path("star/<id>/",views.star_mail,name="star_mail"),
    path("archive/<id>/",views.archive_mail,name="archive_mail"),
    path("delete/<id>/",views.delete_mail,name="delete_mail"),
    path("restore/<id>/",views.restore_mail,name="restore_mail"),
    path("not-spam/<id>/",views.not_spam,name="not_spam"),
    path("permanent-delete/",views.permanently_delete,name="permanent_delete"),
]
