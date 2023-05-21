from django.shortcuts import render,redirect
from .models import Email
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from decouple import config

def mails_table(request):
    if request.user.is_authenticated:
        # get the ,ailbox type from the request params
        mailbox = request.GET.get("mail","inbox")

        # Retrieve emails according to the request params
        if mailbox=="send":
            emails = Email.objects.filter(
                sender=request.user,deleted=False,spam=False
            )
        elif mailbox=="archive":
            emails = Email.objects.filter(
                archived=True,spam=False,deleted=False
            ).filter(Q(sender=request.user) | Q(recipients=request.user))
        elif mailbox == "starred":
            emails = Email.objects.filter(
                starred=True, deleted=False,spam=False
            ).filter( Q(sender=request.user) |Q(recipients=request.user))
        elif mailbox == "trash":
            emails = Email.objects.filter(
                deleted=True
            ).filter( Q(sender=request.user) |Q(recipients=request.user))
        elif mailbox == "spam":
            emails = Email.objects.filter(
                spam=True,deleted=False,archived=False
            ).filter( Q(sender=request.user) |Q(recipients=request.user))
        else:
            emails = Email.objects.filter(
                Q(recipients=request.user), deleted=False,spam=False,archived=False
            )
        page = request.GET.get('page')
        p = Paginator(emails,10)
        emails = p.get_page(page)
        return render(request,'emails/mails_table.html', {'emails': emails,'title':mailbox.capitalize()})
    return redirect("login")

def mail(request,id):
    try:
        mail = Email.objects.get(id=id)
    except Email.DoesNotExist:
        return redirect("home")
    return render(request,'emails/mail.html',{'mail':mail})

def archive_mail(request,id):
    mail = Email.objects.get(id=id)
    if mail.archived:
        mail.archived = False
    else:
        mail.archived = True
    mail.save()
    return redirect("home")

def delete_mail(request,id):
    mail = Email.objects.get(id=id)
    mail.deleted = True
    mail.save()
    return redirect("home")

def restore_mail(request,id):
    mail = Email.objects.get(id=id)
    mail.deleted = False
    mail.save()
    return redirect("home")

def star_mail(request,id):
    referer = request.META.get('HTTP_REFERER')
    referer = referer if referer else "home"
    mail = Email.objects.get(id=id)
    if mail.starred:
        mail.starred = False
    else:
        mail.starred = True
    mail.save()
    return redirect(referer)

def permanently_delete(request):
    emails = Email.objects.filter(
        deleted=True
    ).filter(Q(sender=request.user) | Q(recipients = request.user))
    emails.delete()
    return redirect(f'{reverse("home")}?mail=trash')

def not_spam(request,id):
    referer = request.META.get('HTTP_REFERER')
    referer = referer if referer else "home"
    mail = Email.objects.get(id=id)
    mail.spam = False
    mail.save()
    return redirect(referer)