from django.urls import path
from api.views.user_views import UserList, UserDetails,GroupList
from api.views.event_views import EventList, EventDetails
from api.views.notice_board_views import NoticeBoardList, NoticeBoardDetails
from api.views.user_stuff_views import UserStuffList, UserStuffDetails


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<pk>/user/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('events/', EventList.as_view()),
    path('events/<pk>/event/', EventDetails.as_view()),
    path('notice_boards/', NoticeBoardList.as_view()),
    path('notice_boards/<pk>/notice_board/', NoticeBoardDetails.as_view()),
    path('stuff_users/', UserStuffList.as_view()),
    path('stuff_users/<pk>/stuff_user/', UserStuffDetails.as_view())
]