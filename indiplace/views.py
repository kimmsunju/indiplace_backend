from django.http import Http404
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Member, ArtistInfo, Performance, Genre, FavoriteArtist
from .serializers import MemberSerializer, ArtistInfoSerializer, PerformanceSerializer, GenreSerializer, FavoriteArtistSerializer, ArtistGenreSerializer

class Authorization(APIView):
    def post(self, request, format=None):
        accountType = self.request.data['accountType']
        id = self.request.data['id']
        print(accountType)
        if accountType == 'facebook':
            queryset = Member.objects.get(faceBookId=id)
        elif accountType == 'kakaotalk':
            queryset = Member.objects.get(kakaoTalkId=id)
        else:
            return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

        serializer = MemberSerializer(queryset)
        return Response(serializer.data)

class MemberList(APIView):
    """
    회원가입
    /member
    """
    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


    """
    회원 리스트 조회
    /member
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
    특정 회원 조회
    /member/{pk}
    """
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = MemberSerializer(post)
        return Response(serializer.data)

    """
    특정 회원 수정
    /member/{pk}
    """
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = MemberSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    특정 회원 삭제
    /member/{pk}
    """
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArtistList(APIView):
    def get_queryset(self):
        queryset = ArtistInfo.objects.all()

        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            queryset = queryset.filter(name=keyword)

        return queryset

    def memberUpdate(self):
        try:
            pk = self.request.data['memberId']
            member = Member.objects.get(pk=pk)
            member.memberType = 'A'
            member.save()
        except:
            raise Http404

    """
    아티스트 등록
    /artist
    """
    def post(self, request, format=None):
        serializer = ArtistInfoSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            # member테이블 memberType 변경
            self.memberUpdate()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    """
    아티스트 리스트 조회
    /artist
    """
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ArtistInfoSerializer(queryset, many=True)
        return Response(serializer.data)

class ArtistDetail(APIView):
    def get_object(self, pk):
        try:
            return ArtistInfo.objects.get(pk=pk)
        except ArtistInfo.DoesNotExist:
            raise Http404


    """
    특정 아티스트 조회
    /artist/{pk}
    """
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = ArtistInfoSerializer(post)
        return Response(serializer.data)

    """
    특정 아티스트 수정
    /artist/{pk}
    """
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ArtistInfoSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerformanceList(APIView):
    """
    공연 등록
    /performance
    """
    def post(self, request, format=None):
        serializer = PerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    """
    공연 리스트 조회
    /performance
    """
    def get(self, request, format=None):
        queryset = Performance.objects.all()
        serializer = PerformanceSerializer(queryset, many=True)
        return Response(serializer.data)

class PerformanceDetail(APIView):
    def get_object(self, pk):
        try:
            return Performance.objects.get(pk=pk)
        except Performance.DoesNotExist:
            raise Http404

    """
    특정 공연 조회
    /performance/{pk}
    """
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PerformanceSerializer(post)
        return Response(serializer.data)

    """
    특정 공연 수정
    /performance/{pk}
    """
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PerformanceSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenreList(APIView):
    """
    장르 등록
    /genre
    """
    def post(self, request, format=None):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    """
    장르 리스트 조회
    /genre
    """
    def get(self, request, format=None):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

class ArtistGenreList(APIView): 
    """
    아티스트 장르 등록
    /artistGenre
    """
    def post(self, request, format=None):
        genreList = self.request.data['genreList']
        artistId = self.request.data['artistId']
        for genreId in genreList :
            print(genreId)
            data = {'artistId':artistId, 'genreId':genreId}
            serializer = ArtistGenreSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
 

class FavoriteArtistList(APIView):
    """
    좋아하는 아티스트 등록
    /genre
    """
    def post(self, request, format=None):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

class FavoriteArtistDetail(APIView):
    def get_object(self, pk):
        try:
            return Performance.objects.get(pk=pk)
        except Performance.DoesNotExist:
            raise Http404

    # def get_queryset(self):
    #     keyword = self.request.query_params.get('keyword')
    #
    #     queryset = Performance.objects.filter()

    """
    특정 공연 조회
    /performance/{pk}
    """
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PerformanceSerializer(post)
        return Response(serializer.data)

    """
    특정 공연 수정
    /performance/{pk}
    """
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PerformanceSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
