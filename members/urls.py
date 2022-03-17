from django.urls import path

from .views import member_views

app_name = 'members'

urlpatterns = [
    # member_views
    path('', member_views.index, name='members_list'),
    path('<int:member_id>', member_views.detail, name='members_detail'),
    path('join/', member_views.join, name='members_join'),
    path('modify/<int:member_id>/', member_views.modify, name='members_modify'),
]