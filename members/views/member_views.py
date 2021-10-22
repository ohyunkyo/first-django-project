from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count

from ..forms import MembersForm
from ..models import Member


# 회원목록출력
def index(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    member_list = Member.objects.order_by('-join_at')

    # 페이징 처리
    paginator = Paginator(member_list, 10)
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    context = {'member_list': page_obj, 'page': page, 'last_page': last_page}
    return render(request, 'members/member_list.html', context)


# 회원정보 상세 출력
def detail(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    context = {'member': member}
    return render(request, 'members/member_detail.html', context)


# 회원 추가
def join(request):
    if request.method == 'POST':
        form = MembersForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            member.save()
            return redirect('members:index')
    else:
        form = MembersForm()

    context = {'form': form}
    return render(request, 'members/member_form.html', context)


# 회원 수정
def modify(request, member_id):
    # 질문 수정
    member = get_object_or_404(Member, pk=member_id)

    if request.method == "POST":
        form = MembersForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            return redirect('members:detail', member_id=member.id)
    else:
        form = MembersForm(instance=member)
    context = {'form': form}
    return render(request, 'members/member_form.html', context)
