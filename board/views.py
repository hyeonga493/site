from django.shortcuts import render, redirect
from .models import Board
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    pg = request.GET.get("page", 1)
    #_ 페이지 넘겨오기(default값 1)
    cate = request.GET.get("cate", "")
    #_ 카테고리
    kw = request.GET.get("kw", "")
    #_ 입력칸

    if kw:
        if cate == "sub":
            #_ 과목 이름이면
            b = Board.objects.filter(subject__startswith=kw)
            #_ 입력 값으로 시작하는 과목 정보
        elif cate == "wri":
            #_ 작성자라면
            try:
                from acc.models import User
                #_ User 데이터 가져옴
                u = User.objects.get(username=kw)
                #_ 입력값과 같은 User 가져옴
                b = Board.objects.filter(writer=u)
                #_ 작성자가 같은 파일 가져옴
            except:
                b = Board.objects.none()
                #_ 작성자 일치하는 것 없을 경우 가져오지 않음

        elif cate == "con":
            #_ 내용이라면
            b = Board.objects.filter(content__contains=kw)
            #_ 입력값을 포함한 내용을 가진 데이터 가져옴
    else:
        b = Board.objects.all()
        #_ 입력이 없을 경우, 모든 데이터 가져옴

    b = b.order_by("-pubdate")
    #_ 수정된 날짜를 기준으로 정렬

    pag = Paginator(b, 3)
    #_ 데이터 전부를 한 페이지당 3개씩 나타나도록 정의
    obj = pag.get_page(pg)
    #_ 페이지에 담긴 정보
    context = {
        "bset" : obj,
        "kw" : kw,
        "cate" : cate
    }
    return render(request, "board/index.html", context)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    #_ 수정할 정보 확인
    if request.user != b.writer:
        #_ 작성자와 접근자가 다르다면 접근 불가
        return redirect("board:index")
        
    if request.method == "POST":
        #_ 정보입력 받은 경우
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s,c
        b.save()
        messages.success(request, f'Update data!')
        return redirect("board:detail", bpk)
        #_ 수정한 데이터 페이지로 넘어가는 것이 자연스러움
        
    context = {
        "b" :b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
        messages.success(request, f'Delete')
    else:
        messages.warning(request, f'Wrong way')
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    context = {
        "b" : b
    }
    return render(request, "board/detail.html", context)

