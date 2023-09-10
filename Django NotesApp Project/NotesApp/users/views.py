from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Note

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created, You can Login Now!')
            return redirect('/login')
    else:
        form = UserRegisterForm()    
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)



@login_required
def notes(request):
    user = request.user
    docid = int(request.GET.get('docid', 0))
    documents = Note.objects.filter(user=user)

    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content','')

        if docid > 0:
            document = Note.objects.get(pk=docid, user=user)
            document.title = title
            document.content = content
            document.save()
            return redirect('/notes/?docid=%i' % docid)
        else:
            document = Note.objects.create(title=title, content=content, user=user)
            return redirect('/notes/?docid=%i' % document.id)


    if docid > 0:
        document = Note.objects.get(pk=docid, user=user)
    else:
        document = ''

    context = {
        'docid':docid,
        'documents':documents,
        'document':document
    }
    return render(request, 'users/notes.html', context)

@login_required
def delete_note(request, docid):
    user = request.user
    document = Note.objects.get(pk=docid, user=user)
    document.delete()
    messages.success(request, f'Note Deleted Successfully')
    return redirect('/notes/?docid=0')