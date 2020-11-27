from django.urls import path
from rest_framework import routers

from api.views.user_views import UserList, UserDetails, GroupList, UserByUsernameList
from api.views.event_views import EventList, EventDetails
from api.views.notice_board_views import NoticeBoardList, NoticeBoardDetails
from api.views.user_stuff_views import UserStuffList, UserStuffDetails
from api.views.club_facility_views import ClubFacilityList, ClubFacilityDetails
from api.views.club_facility_detail_views import  ClubFacilityDeailsList, ClubFacilityDetailDetails


router = routers.DefaultRouter()
router.register(r'opt_operation', UserByUsernameList)
router.register(r'users', UserList)
router.register(r'stuff_users', UserStuffList)


urlpatterns = [
    #path('users/', UserList,name='users'),
    #path('users/<pk>/user/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('events/', EventList.as_view()),
    path('events/<pk>/event/', EventDetails.as_view()),
    path('notice_boards/', NoticeBoardList.as_view()),
    path('notice_boards/<pk>/notice_board/', NoticeBoardDetails.as_view()),
    #path('stuff_users/', UserStuffList.as_view()),
    #path('stuff_users/<pk>/stuff_user/', UserStuffDetails.as_view()),
    path('club_facilities/', ClubFacilityList.as_view()),
    path('club_facilities/<pk>/club_facility/', ClubFacilityDetails.as_view()),
    path('club_facility_detail_details/', ClubFacilityDeailsList.as_view()),
    path('club_facility_detail_details/<pk>/club_facility_detail_detail/', ClubFacilityDetailDetails.as_view())
]

urlpatterns += router.urls
