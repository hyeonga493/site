from django.shortcuts import render,redirect
from .models import Topic, Choice

def delete(request,tpk):
    tp = Topic.objects.get(id=tpk)
    if tp.maker == request.user:
        tp.delete()
    return redirect('vote:index')

def cancle(request,tpk):
    #_ 무르기 기능
    u = request.user
    tp = Topic.objects.get(id=tpk)
    #_ 유저의 입장에서 n:n 관계
    #_ 유저가 고른 것 중 tpk를 가져와야 함
    u.choice_set.get(top=tp).choicer.remove(u)
    tp.voter.remove(u)
    #_ 유저가 골랐던 것 중에 토픽이 같은 것을 선택해서 제거한다.
    return redirect('vote:detail',tpk)

def vote(request, tpk):
    tp = Topic.objects.get(id=tpk)
    if not request.user in tp.voter.all():
        tp.voter.add(request.user)
        cpk = request.POST.get('cho')
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)

    return redirect('vote:detail', tpk)

'''def vote(request, tpk):
    tp = Topic.objects.get(id=tpk)
    tp.voter.add(request.user)
    cpk = request.POST.get('cho')
    Choice.objects.get(id=cpk)
    c.choicer.add(request.user)
    #_ 중복 투표 불가, 다중 투표 가능
    return redirect('vote/detail.html', tpk)'''

def detail(request, tpk):
    tp = Topic.objects.get(id=tpk)
    ch = tp.choice_set.all()
    context = {
        'tp' : tp,
        'ch' : ch,
    }
    return render(request, 'vote/detail.html', context)

def create(request):
    if request.method=="POST":
        s = request.POST.get('sub')
        c = request.POST.get('con')
        t = Topic(subject=s, maker=request.user, content=c)
        t.save()
        
        cn = request.POST.getlist('cname')
        cc = request.POST.getlist('ccom')
        #_ 리스트는 for문으로 돌리지 않는다
        #_ list( zip( A, B ) )
        #_ 같은 인덱스끼리 튜플로 묶어준다
        print(cn,cc)
        for name, com in zip(cn, cc):
            Choice(top=t, name=name, comment=com).save()
        return redirect('vote:index')
    return render(request, 'vote/create.html')

def index(request):
    tp = Topic.objects.all()
    context = {
        'tp' : tp
    }
    return render(request, 'vote/index.html', context)