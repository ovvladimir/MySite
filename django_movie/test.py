import os
import sys
import django
p = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(p)
os.environ["DJANGO_SETTINGS_MODULE"] = "django_movie.settings"

django.setup()

try:
    from movies.models import Movie, Actor, Genre, Rating, Category, Reviews, Videos
    from django.urls import reverse
except (ImportError, BaseException):
    pass

"""
s = Videos.objects.filter(movie_id=True).values('video').first()['video']
a = Videos.objects.all().values().first()['video']
b = list(Videos.objects.all().values('video'))[0]['video']
# c = b[0]['video']

print(a)
print(b)
print(s)

z = Movie.objects.all().values('category')
zz = Movie.objects.filter(category=True)
zzz = Category.objects.all().values('name')
zzzz = Category.objects.all().values()

print(z)
print(zz)
print(zzz)
print(zzzz)
"""
print("1 --------------------------------")
sss = Rating.objects.order_by("movie")[:]
print(sss)
for i in sss:
    s = str(i).split(' - ')
    print(s)
    x = Movie.objects.get(title=str(s[-1]))
    print(x)
    print(x.get_absolute_url())
print("1 --------------------------------")
print("2 --------------------------------")
ss = Rating.objects.all().values("star", "movie")
print(ss)
for key in ss:
    print(key)
    x = Movie.objects.get(pk=key["movie"])
    print(x)
    print(x.get_absolute_url())
print("2 --------------------------------")
print("3 --------------------------------")
dict_star = {key['star']: key['movie'] for key in ss}
print(dict_star, "!!!!!!!!!!!!!")
for keys, vol in dict_star.items():
    print(keys, vol)
x = Movie.objects.get(pk=1)
print(x, "///", type(x))
xx = x.get_absolute_url()
print(xx)
print("3 --------------------------------")
print("4 --------------------------------")
mov_list = []
rat_list = []
mov = Rating.objects.all().values()
print(mov)
for m in mov:
    mov_list.append(Movie.objects.get(pk=m["movie_id"]).get_absolute_url())
    rat_list.append(m["star_id"])
print(mov_list)
print(rat_list)
print("4 --------------------------------")
print("5 --------------------------------")
mov = Rating.objects.all().values("star_id")
print(mov)
for i in mov:
    m = i["star_id"]
    print(m, type(m))
print("5 --------------------------------")

print(Movie.objects.filter(year=1991))
print(Rating.objects.filter(star=4))
print(Movie.objects.get(pk=1))
print(Movie.objects.filter(id=1))
print(Rating.objects.filter(star=5))
print(Rating.objects.filter(movie=1).values('star_id')[0]['star_id'])

ss = Rating.objects.all().values("star", "movie")
dict_star = {key['movie']: key['star'] for key in ss}
print(dict_star[1])
m = list(Movie.objects.all().values("poster"))
print(m)
'''
def get_absolute_url(self):
    return reverse("movie_detail", kwargs={"slug": self.url})
#print(get_absolute_url(x))

z = Rating.objects.all().values("movie")
print(z)
x = Rating.objects.order_by("movie")[:]
print(x)
'''
