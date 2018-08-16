from rest_framework import serializers
from .models import Member, ArtistInfo, Performance, Genre

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ArtistInfoSerializer(serializers.ModelSerializer):
    memberId = MemberSerializer()

    class Meta:
        model = ArtistInfo
        fields = ('memberId', 'location', 'faceBook', 'youtube', 'instagram', 'image')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    memberId = ArtistInfoSerializer()

    class Meta:
        model = Performance
        fields = ('memberId', 'genre', 'registed_dt', 'startTime', 'endTime', 'location', 'lat', 'lot')
