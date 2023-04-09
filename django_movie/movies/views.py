# from django.conf import settings
# from django.db import models
from django.db.models import Q  # , OuterRef, Subquery, Case, When
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Actor, Genre, Rating  # , Category, Reviews
from .forms import ReviewForm, RatingForm


class RatingView:
    def title(self):
        return str("Рейтинг")

    def list_stars(self):
        list_of_stars = range(1, 6)
        return list_of_stars

    def get_rating(self):
        r = Rating.objects.all().values("star", "movie")
        dict_star = {key['movie']: key['star'] for key in r}
        return dict_star

    def get_poster(self):
        return Movie.objects.filter(draft=False).values("poster")


class GenreYear:
    """Темы и года выхода уроков"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class RatingLessonView(RatingView, ListView, GenreYear):
    """Фильтр рейтингов"""
    paginate_by = 6

    def get_queryset(self):
        mov_id = Rating.objects.filter(star__in=self.request.GET.getlist("stars")).values('movie')
        queryset = Movie.objects.filter(
            Q(id__in=mov_id)).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["star"] = ''.join([f"star={x}&" for x in self.request.GET.getlist("stars")])
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MoviesView(RatingView, GenreYear, ListView):
    """Список уроков"""
    model = Movie
    queryset = Movie.objects.filter(draft=False).order_by('id')
    paginate_by = 3  # кол-во картинок на главной странице


class MovieDetailView(RatingView, GenreYear, DetailView):
    """Полное описание урока"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(RatingView, GenreYear, DetailView):
    """Вывод информации о авторе"""
    model = Actor
    template_name = 'movies/author.html'
    slug_field = "name"


class FilterMoviesView(RatingView, ListView, GenreYear):
    """Фильтр уроков"""
    paginate_by = 6

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр уроков в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга уроку"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(RatingView, ListView, GenreYear):
    """Поиск уроков"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
