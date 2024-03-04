from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import Count,Sum,Avg,Min,Max
from django.core.paginator import Paginator

from .models import Friend,Message
from .forms import FriendForm,FindForm,MessageForm

def message(request, page=1):
    if (request.method == 'POST'):
        form = MessageForm(request.POST)
        form.save()
    data = Message.objects.all().order_by("-pub_date")
    paginator = Paginator(data, 5)
    params = {
        'title': 'Message',
        'form': MessageForm(),
        'data': paginator.get_page(page),
    }
    return render(request, 'hello/message.html', params)

def index(request, num=1):
    data = Friend.objects.all()
    page = Paginator(data, 3)
    params = {
        'title': 'Hello',
        'message':'',
        'data': page.get_page(num),
    }
    return render(request, 'hello/index.html', params)

def create(request):
    if (request.method == 'POST'):
        # obj = Friend() ←これ冗長。
        friend = FriendForm(request.POST) #わざわざ空のインスタンス作らないでも自動で生成してくれる。
        friend.save() #これは大事。レコードを保存してる。
        return redirect(to='/hello') #/helloのリクエストを投げてくれる
    params = {
        'title': 'Hello',
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)

def edit(request, num):
    obj = Friend.objects.get(id=num)
    print(obj.id)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id':num,
        'form': FriendForm(instance=obj),
    }
    return render(request, 'hello/edit.html', params)

def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id':num,
        'obj': friend,
    }
    return render(request, 'hello/delete.html', params)


def find(request):
    if (request.method == 'POST'):
        msg = 'search result:'
        form = FindForm(request.POST)
        find = request.POST['find']
        list = find.split()
        print(list)
        data = Friend.objects.all()[int(list[0]):int(list[1])]    #☆
    else:
        msg = 'search words...'
        form = FindForm()
        data =Friend.objects.all()
    params = {
        'title': 'Hello',
        'message': msg,
        'form':form,
        'data':data,
    }
    return render(request, 'hello/find.html', params)

from .forms import CheckForm    #☆

def check(request):
    params = {
        'title': 'Hello',
        'message':'check validation.',
        'form': FriendForm(),
    }
    if (request.method == 'POST'):
        # obj = Friend()
        form = FriendForm(request.POST)
        print(form)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'no good.'
    return render(request, 'hello/check.html', params)