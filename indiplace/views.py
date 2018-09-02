from django.http import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.exceptions import APIException
from .models import Member, ArtistInfo, Performance, FavoriteArtist, Comment
from .serializers import MemberSerializer, ArtistInfoSerializer, PerformanceSerializer, PostPerformanceSerializer, FavoriteArtistSerializer, PostFavoriteArtistSerializer, CommentSerializer, CommentListSerializer
import datetime

class Resultset(APIView):
    @staticmethod
    def resultset(key, data):
        print('resultset')
        return Response({'key':key, 'message':data})
    
class CustomApiException(APIException):

    #public fields
    key = None
    message = None
    detail = ';;;;'
    status_code = None

    # create constructor
    def __init__(self, key, message):
        #override public fields
        CustomApiException.key = key
        CustomApiException.message = message

class Authorization(APIView):
    renderer_classes = (JSONRenderer, )

    def resultset(self, key, data):
        print('resultset')
        return Response({'key':key, 'message':data})
        
    def post(self, request, format=None):
        accountType = self.request.data['accountType']
        id = self.request.data['id']
        try:
            if accountType == 'facebook':
                queryset = Member.objects.get(faceBookId=id)
            elif accountType == 'kakaotalk':
                queryset = Member.objects.get(kakaoTalkId=id)
            else:
                return Response({'key': False, 'message': 'accountType 오류'}, content_type='application/json; charset=utf-8')

            serializer = MemberSerializer(queryset)
            return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
        except Member.DoesNotExist:
            return Response({'key': False, 'message': '해당 계정이 없음'}, content_type='application/json; charset=utf-8')

class MemberList(APIView):
    renderer_classes = (JSONRenderer, )

    """
    회원가입
    /member
    """
    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        return Response({'key': False, 'message': serializer.errors})


    """
    회원 리스트 조회
    /member
    """
    def get(self, request, format=None):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')

class MemberDetail(APIView):
    renderer_classes = (JSONRenderer, )

    def get_object(self, pk):
        try:
            print('ffsssssssssssssssssss')
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            # return Member.objects.get(pk=pk)
            raise CustomApiException(False, 'no data')
            print('ffsssssssssssssssssss')
            # return Response({'key': False, 'message': ''})

    """
    특정 회원 조회
    /member/{pk}
    """
    def get(self, request, pk):
        try:
            post = Member.objects.get(pk=pk)
            serializer = MemberSerializer(post)
            return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
        except Member.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})


    """
    특정 회원 수정
    /member/{pk}
    """
    def put(self, request, pk, format=None):
        try:
            post = Member.objects.get(pk=pk)
            serializer = MemberSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
            return Response({'key': False, 'message': serializer.errors})
        except Member.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})
    """
    특정 회원 삭제
    /member/{pk}
    """
    def delete(self, request, pk, format=None):
        try:
            post = Member.objects.get(pk=pk)
            post.delete()
            return Response({'key': True, 'message': '삭제 완료'}, status=status.HTTP_204_NO_CONTENT, content_type='application/json; charset=utf-8')
        except Member.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})

class ArtistList(APIView):
    renderer_classes = (JSONRenderer, )

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
        if serializer.is_valid():
            serializer.save()
            self.memberUpdate() # member테이블 memberType 변경
            return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        return Response({'key': False, 'message': serializer.errors})

    """
    아티스트 리스트 조회
    /artist
    """
    def get(self, request, *args, **kwargs):
        queryset = ArtistInfo.objects.all()

        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            queryset = queryset.filter(name__icontains=keyword)
        serializer = ArtistInfoSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')


class ArtistDetail(APIView):
    renderer_classes = (JSONRenderer, )

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
        try:
            post = ArtistInfo.objects.get(pk=pk)
            serializer = ArtistInfoSerializer(post)
            return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
        except ArtistInfo.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})
            

    """
    특정 아티스트 수정
    /artist/{pk}
    """
    def put(self, request, pk, format=None):
        try:
            post = ArtistInfo.objects.get(pk=pk)
            serializer = ArtistInfoSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
            return Response({'key': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ArtistInfo.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})

class PerformanceList(APIView):
    renderer_classes = (JSONRenderer, )
    
    def runGCM(self, memberDevicetoken):
        gcm = GCM('AIzaSyACe5g4v3-XKBDRDhK2-ORKBtPb272kj4E')
        data = {'param1': 'value1', 'param2': 'value2'}

        # Downstream message using JSON request
        reg_ids = memberDevicetoken
        response = gcm.json_request(registration_ids=reg_ids, data=data)

        # Downstream message using JSON request with extra arguments
        res = gcm.json_request(
            registration_ids=reg_ids, data=data,
            collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
        )

        # Topic Messaging
        topic = 'topic name'
        gcm.send_topic_message(topic=topic, data=data)
    
    def getMemberId(self, artistId):
        queryset = FavoriteArtist.objects.filter(artistId=artistId)
        serializer = FavoriteArtistSerializer(queryset, many=True)
        memberDevicetoken = []
        for data in serializer.data:
            queryset = Member.objects.get(pk=data['memberId'])
            serializer = MemberSerializer(queryset)
            memberDevicetoken.append(serializer.data['deviceToken'])
        
        if len(memberDevicetoken) > 0:
            self.runGCM(memberDevicetoken)
        

    """
    공연 등록
    /performance
    """
    def post(self, request, format=None):
        serializer = PostPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # self.getMemberId(serializer.data['artistId'])
            return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        return Response({'key': False, 'message': serializer.errors})

    """
    공연 리스트 조회
    /performance
    """
    def get(self, request, format=None):
        queryset = Performance.objects.all()

        location = self.request.GET.get('location', None)
        genre = self.request.GET.get('genre', None)
        if location is not None:
            queryset = queryset.filter(location=location)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        serializer = PerformanceSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')

class PerformanceView(APIView):
    renderer_classes = (JSONRenderer, )

    """
    선택한 지역 공연리스트(5개)
    """
    def get(self, request, format=None):
        queryset = Performance.objects.all()
        
        location = self.request.GET.get('location', None)
        if type is not None:
            queryset = queryset.filter(startTime__gt=datetime.datetime.now()).filter(location=location).order_by('startTime')
        serializer = PerformanceSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data[0:5]}, content_type='application/json; charset=utf-8')

class PerformanceRecent(APIView):
    renderer_classes = (JSONRenderer, )

    """
    최근 공연리스트(5개)
    """
    def get(self, request, format=None):
        queryset = Performance.objects.filter(startTime__gt=datetime.datetime.now()).order_by('startTime')
        serializer = PerformanceSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data[0:5]}, content_type='application/json; charset=utf-8')

class PerformanceFavor(APIView):
    renderer_classes = (JSONRenderer, )

    def favor(self, pk):
        queryset = FavoriteArtist.objects.filter(memberId=pk)
        serializer = FavoriteArtistSerializer(queryset, many=True)
        artistList = []
        for data in serializer.data:
            artistList.append(data['artistId'])
        return artistList

    """
    좋아하는 아티스트 공연리스트(5개)
    """
    def get(self, request, pk):
        artistList = self.favor(pk)
        queryset = Performance.objects.filter(artistId__in=artistList).filter(startTime__gt=datetime.datetime.now()).order_by('startTime')
        serializer = PerformanceSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data[0:5]}, content_type='application/json; charset=utf-8')

class PerformanceDetail(APIView):
    renderer_classes = (JSONRenderer, )

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
        try:
            post = Performance.objects.get(pk=pk)
            serializer = PerformanceSerializer(post)
            return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
        except Performance.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})

    """
    특정 공연 수정
    /performance/{pk}
    """
    def put(self, request, pk, format=None):
        try:
            post = Performance.objects.get(pk=pk)
            serializer = PostPerformanceSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
            return Response({'key': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'key': False, 'message': 'No data'})

# class GenreList(APIView):
#     """
#     장르 등록
#     /genre
#     """
#     def post(self, request, format=None):
#         serializer = GenreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

#     """
#     장르 리스트 조회
#     /genre
#     """
#     def get(self, request, format=None):
#         queryset = Genre.objects.all()
#         serializer = GenreSerializer(queryset, many=True)
#         return Response({'key': True, 'message': serializer.data})

# class ArtistGenreList(APIView): 
#     """
#     아티스트 장르 등록
#     /artistGenre
#     """
#     def post(self, request, format=None):
#         genreList = self.request.data['genreList']
#         artistId = self.request.data['artistId']
#         for genreId in genreList :
#             print(genreId)
#             data = {'artistId':artistId, 'genreId':genreId}
#             serializer = ArtistGenreSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#         return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED)
 

class FavoriteArtistList(APIView):
    renderer_classes = (JSONRenderer, )

    """
    좋아하는 아티스트 등록
    /favorite
    """
    def post(self, request, format=None):
        serializer = PostFavoriteArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        return Response({'key': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteArtistDetail(APIView):
    renderer_classes = (JSONRenderer, )

    """
    좋아하는 아티스트 조회
    /favorite/{pk}
    """
    def get(self, request, pk):
        queryset = FavoriteArtist.objects.filter(memberId=pk)
        serializer = FavoriteArtistSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
    """
    좋아하는 아티스트 삭제
    /favorite/{pk}
    """
    def delete(self, request, pk):
        try:
            queryset = FavoriteArtist.objects.filter(pk=pk)
            queryset.delete()
            return Response({'key': True, 'message': '삭제 완료'}, status=status.HTTP_204_NO_CONTENT, content_type='application/json; charset=utf-8')
        except FavoriteArtist.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})


class CommentList(APIView):
    renderer_classes = (JSONRenderer, )

    """
    코멘트 등록
    /comment
    """
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'key': True, 'message': serializer.data}, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        return Response({'key': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    renderer_classes = (JSONRenderer, )

    """
    코멘트 리스트 조회
    /comment/{pk}
    """
    def get(self, request, pk):
        queryset = Comment.objects.filter(artistId=pk)
        serializer = CommentListSerializer(queryset, many=True)
        return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')

    """
    특정 코멘트 수정
    /comment/{pk}
    """
    def put(self, request, pk, format=None):
        try:
            post = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'key': True, 'message': serializer.data}, content_type='application/json; charset=utf-8')
            return Response({'key': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'key': False, 'message': 'No data'})

    """
    특정 코멘트 삭제
    /comment/{pk}
    """
    def delete(self, request, pk, format=None):
        try:
            post = Comment.objects.get(pk=pk)
            post.delete()
            return Response({'key': True, 'message': '삭제 완료'}, status=status.HTTP_204_NO_CONTENT, content_type='application/json; charset=utf-8')
        except Member.DoesNotExist:
            return Response({'key': False, 'message': 'No data'})