from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models.aggregates import Avg

from .models import Product, Review, Proposal
from .forms import ProductForm, ReviewForm, ProposalForm

# 상품 등록
@login_required
@require_http_methods(['GET', 'POST'])
# @permission_required('tour.can_make_product')
def create_product(request):
    if not request.user.groups.filter(name="guide").exists():
        return redirect('home')
    
    if request.method == 'GET':
        form = ProductForm()
    else:
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.writer = request.user
            product.save()
            return redirect('tour:product_detail', product.pk)

    return render(request, 'tour/form.html',{
        'form': form,
    })

# 상품 4개씩 보이게 하기
@require_safe
def product_index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tour/index.html', {
        'page_obj': page_obj,
    })

# # 상품 10개씩 보이기
# @require_safe
# def product_index(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 10)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     return render(request, 'tour/index.html', {
#         'page_obj': page_obj,
#     })

# 내 프로필 들어가서 상품 관련 정보 보이기
@require_safe
def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    reviews = product.reviews.all()
    form = ReviewForm()
    
    avgscores = Review.objects.filter(product_id=product.pk).aggregate(average_score = Avg("score"))
    if avgscores['average_score'] != None:
        avgscores = round(avgscores['average_score'], 1)
    else:
        avgscores = 0.0
    
    is_wishlist = product.wishlist.filter(pk=request.user.pk)

    return render(request, 'tour/detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'avgscore': avgscores,
        'is_wishlist': is_wishlist,
    })
    


# 상품 수정
@login_required
@require_http_methods(['GET', 'POST'])
def update_product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    
    if request.user != product.writer:
        return redirect('tour:product_detail', product.pk)
    
    if request.method == 'GET':
        form = ProductForm(instance=product)
    else:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = product.save()
            return redirect('tour:product_detail', product_pk)
    return render(request, 'tour/form.html', {
        'form': form
    })
    
# 상품 삭제
@login_required
@require_POST
def delete_product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    
    if request.user != product.writer:
        return redirect('tour:product_detail', product.pk)
    product.delete()
    return redirect('tour:product_index')

# 리뷰 생성
@login_required
@require_POST
def create_review(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.writer = request.user
        review.save()
        return redirect('tour:product_detail', product.pk)

# 리뷰 삭제
@login_required
@require_POST
def delete_review(request, product_pk, review_pk):
    product = get_object_or_404(Product, pk=product_pk)
    review = get_object_or_404(Review, pk=review_pk)
    
    if request.user != review.writer:
        return redirect('tour:product_detail', product.pk)
    review.delete()
    return redirect('tour:product_detail', product.pk)
 
# 찜하기
@login_required
@require_POST
def wishlist(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    user = request.user
    
    if product.wishlist.filter(pk=user.pk).exists():
        product.wishlist.remove(user)
    else:
        product.wishlist.add(user)
    return redirect('tour:product_detail', product.pk)
   

# @login_required 
# def proposal_tour(request, product_pk):
#     product = get_object_or_404(Product, pk=product_pk)
#     proposal = request.user
#     # user = request.user
    
#     if request.user.is_authenticated:
#         if request.user != product.writer:
#             # 내 프로필에 신청 기록 띄우기
#             if product.proposal.filter(pk=proposal.pk).exists():
#                 product.proposal.remove(request.user)
#                 messages.add_message(proposal.request, messages.ERROR, '이미 신청된 투어입니다.')
#             else:
#                 product.proposal.add(proposal.pk)
#                 messages.add_message(proposal.reqeust, messages.SUCCESS, '신청이 완료되었습니다.')
#         return render('tour/tour_proposal') 
#     # 가이드 프로필에 제안 알림
    
#     return redirect('tour:product_detail', proposal.username)

# 투어 요청하기
@login_required 
def proposal_tour(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    proposal = request.user
    
    if request.user.is_authenticated:
        if request.user != product.writer:
            # 내 프로필에 신청 기록 띄우기
            if product.proposal.filter(pk=proposal.pk).exists():
                product.proposal.remove(request.user)
                messages.add_message(proposal.request, messages.ERROR, '이미 신청된 투어입니다.')
            else:
                product.proposal.add(proposal.pk)
                messages.add_message(proposal.request, messages.SUCCESS, '신청이 완료되었습니다.')
        return render(request, 'tour/tour_proposal.html') 
    # 가이드 프로필에 제안 알림
    
    return redirect('tour/product_detail/')

    
# 요청 수락하기
@login_required
def accept_proposal(request, proposal_pk):
    proposal = get_object_or_404(Proposal, pk=proposal_pk)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('accounts:login')
        
        if proposal.product.writer != request.user:
            messages.error(request, '예약 수락 권한이 없습니다.')
            return redirect('home')
        
        proposal.accepted = True
        proposal.save()
        messages.success(request, '예약을 수락했습니다.')

    return redirect('home')

# 요청 거절하기
@login_required
def reject_proposal(request, proposal_pk):
    proposal = get_object_or_404(Proposal, pk=proposal_pk)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('accounts:login')
        
        if proposal.product.writer != request.user:
            messages.error(request, '예약 거절 권한이 없습니다.')
            return redirect('home')
        
        proposal.delete()
        messages.success(request, '예약을 거절했습니다.')

    return redirect('home')


    
    # 수락한 요청 가이드 프로필에 띄우기
    
    # 투어리스트에게 안내 문자
    

@login_required
def search(request):
    if request.method == 'POST':  # POST 말고 GET으로 보내기
        searched = request.POST['searched']
        product = Product.objects.filter(country__contains=searched)
        return render(request, 'tour/search.html', {
            'searched': searched, 
            'product': product,})
    else:
        return render(request, 'tour/search.html', {})