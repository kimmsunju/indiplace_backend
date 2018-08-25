from rest_framework import serializers
from .models import Member, ArtistInfo, Performance, Genre, FavoriteArtist, ArtistGenre


class ArtistInfoSerializer(serializers.ModelSerializer):
    # memberId = MemberSerializer()

    class Meta:
        model = ArtistInfo
        fields = ('memberId', 'artistLocation', 'faceBook', 'youtube', 'instagram', 'image')
        # fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    artist_info = ArtistInfoSerializer(read_only=True, many=False)
    class Meta: 
        model = Member
        fields = ('id', 'name', 'emailAddress', 'sex', 'year', 'location', 'memberType', 'artist_info')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ArtistGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistGenre
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    memberId = ArtistInfoSerializer()

    class Meta:
        model = Performance
        fields = ('memberId', 'genre', 'registed_dt', 'startTime', 'endTime', 'location', 'lat', 'lot')

class FavoriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArtist
        fields = '__all__'
