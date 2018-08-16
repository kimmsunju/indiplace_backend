from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Member
from .serializers import MemberSerializer

class MemberList(APIView):
    """
    게시물 생성
    /post/
    """
    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


    """
    게시물 조회
    /post/
    """
    def get(self, request, format=None):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data)

class MemberDetail(APIView):
    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    """
    특정 게시물 조회
    /post/{pk}/
    """
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = MemberSerializer(post)
        return Response(serializer.data)

    """
    특정 게시물 수정
    /post/{pk}/
    """
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = MemberSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    특정 게시물 삭제
    /post/{pk}/
    """
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
