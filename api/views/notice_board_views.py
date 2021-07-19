from rest_framework import generics, permissions
from api.serializer.notice_board_serializers import NoticeBoardSerializer
from ..models import NoticeBoard
from django.contrib.auth import get_user_model

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class NoticeBoardList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = NoticeBoard.objects.all().order_by('-id')
    serializer_class = NoticeBoardSerializer

class NoticeBoardDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = NoticeBoard.objects.all().order_by('-id')
    serializer_class = NoticeBoardSerializer