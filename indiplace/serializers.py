from rest_framework import serializers
from .models import Member, ArtistInfo, Performance, FavoriteArtist, Comment


class ArtistInfoSerializer(serializers.ModelSerializer):
    # memberId = MemberSerializer()

    class Meta:
        model = ArtistInfo
        # fields = ('id', 'memberId', 'name', 'artistLocation', 'faceBook', 'youtube', 'instagram', 'image')
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    artist_info = ArtistInfoSerializer(read_only=True, many=False)
    class Meta: 
        model = Member
        fields = ('id', 'name', 'emailAddress', 'sex', 'year', 'location', 'memberType', 'artist_info')

class MemberSimpleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Member
        fields = ('id', 'name')

# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = '__all__'

# class ArtistGenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArtistGenre
#         fields = '__all__'

class PostPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('artistId', 'genre', 'registed_dt', 'startTime', 'endTime', 'location', 'lat', 'lot')

class PerformanceSerializer(serializers.ModelSerializer):
    artistId = ArtistInfoSerializer()

    class Meta:
        model = Performance
        fields = ('artistId', 'genre', 'registed_dt', 'startTime', 'endTime', 'location', 'lat', 'lot')

class FavoriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArtist
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # memberId = MemberSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class CommentListSerializer(serializers.ModelSerializer):
    memberId = MemberSimpleSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'memberId','content')

