from django.urls import path
from . import views

app_name = 'tour'

urlpatterns = [
    # /tour/
    path('', views.product_index, name='product_index'),
    
    # /tour/create/ 상품 생성
    path('create/', views.create_product, name='create_product'),
    # /tour/1/ 상품 정보
    path('<int:product_pk>/', views.product_detail, name='product_detail'),
    # /tour/1/update/ 상품 수정
    path('<int:product_pk>/update/', views.update_product, name='update_product'),
    # /tour/1/delete/ 상품 삭제
    path('<int:product_pk>/delete/', views.delete_product, name='delete_product'),
    
    # /tour/1/reviews/create/ 리뷰 작성
    path('<int:product_pk>/reviews/create/', views.create_review, name='create_review'),
    # /tour/1/reviews/1/delete/ 리뷰 삭제
    path('<int:product_pk>/reviews/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    
    # /tour/1/wishlist/ 위시리스트
    path('<int:product_pk>/wishlist/', views.wishlist, name='wishlist'),
    
    # /tour/1/proposal/ 투어 요청
    path('<int:product_pk>/proposal/', views.proposal_tour, name='proposal_tour'),
    # /tour/1/accept/ 투어 수락
    path('<int:product_pk>/accept/', views.accept_proposal, name='accept_proposal'),
    
    # /tour/search/
    path('search/', views.search, name='search'),

    
]
