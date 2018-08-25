from django.db import models

class Member(models.Model):
    faceBookId = models.CharField(max_length=10, null=True)
    kakaoTalkId = models.CharField(max_length=15, null=True)
    name = models.CharField(max_length=10)
    emailAddress = models.EmailField(max_length=254)
    sex = models.CharField(max_length=1)
    year = models.IntegerField()
    location = models.CharField(max_length=10)
    memberType = models.CharField(max_length=10, default='U')
    deviceToken = models.CharField(max_length=30)
    registed_dt = models.DateTimeField(auto_now_add=True)

class ArtistInfo(models.Model):
    memberId = models.OneToOneField('Member', related_name='artist_info', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    registed_dt = models.DateTimeField(auto_now_add=True)
    artistLocation = models.CharField(max_length=10)
    faceBook = models.CharField(max_length=50, null=True)
    youtube = models.CharField(max_length=50, null=True)
    instagram = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    genre = models.IntegerField()
    is_allowed = models.BooleanField(default=False)
    

class Performance(models.Model):
    artistId = models.ForeignKey('ArtistInfo', on_delete=models.CASCADE)
    genre = models.IntegerField()
    registed_dt = models.DateTimeField(auto_now_add=True)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.CharField(max_length=10)
    lat = models.IntegerField()
    lot = models.IntegerField()

class FavoriteArtist(models.Model):
    memberId = models.ForeignKey('Member', on_delete=models.CASCADE)
    artistId = models.ForeignKey('ArtistInfo', on_delete=models.CASCADE)

# class Genre(models.Model):
#     name = models.CharField(max_length=20)

# class ArtistGenre(models.Model):
#     artistId = models.ForeignKey('ArtistInfo', on_delete=models.CASCADE)
#     genreId = models.ForeignKey('Genre', on_delete=models.CASCADE)

class Comment(models.Model):
    memberId = models.ForeignKey('Member', on_delete=models.CASCADE)
    artistId = models.ForeignKey('ArtistInfo', on_delete=models.CASCADE)
