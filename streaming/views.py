from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from streaming.models import Movie, Review, UserProfile, SubscriptionPlan
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from streaming.models import Movie
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def user_subscription(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    subscription = user_profile.subscription_plan
    movies = subscription.movies.all()
    return render(request, 'streaming/user_subscription.html', {'subscription': subscription, 'movies': movies})


"""def movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'streaming/movie.html', {'movie': movie})"""


def movie(request, movie_id):
    global user_profile
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.all()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_review = reviews.filter(user=user_profile).first()
    else:
        user_review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user_profile
            review.movie = movie
            review.save()
            return HttpResponseRedirect(reverse('streaming:movie', args=[movie_id]))
    else:
        form = ReviewForm() if not user_review else None

    return render(request, 'streaming/movie.html',
                  {'movie': movie, 'reviews': reviews, 'form': form, 'user_review': user_review})


def index(request):
    movies = Movie.objects.annotate(
        average_rating=Avg('reviews__rating'),
        num_ratings=Count('reviews__rating')
    ).all()
    return render(request, 'streaming/index.html', {'movies': movies})


"""def movie(request, movie_id):
    try:
        print(Movie.objects.get(pk=movie_id))
        movie = Movie.objects.get(pk=movie_id)
        return render(request, 'streaming/movie.html', {'movie': movie})
    except ObjectDoesNotExist:
        raise Http404('Movie not found')"""

"""def user_reviews(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    reviews = Review.objects.filter(user=user)
    return render(request, 'streaming/user_reviews.html', {'user': user, 'reviews': reviews})"""


def user_reviews(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    reviews = Review.objects.filter(user=user_profile)
    return render(request, 'streaming/user_reviews.html', {'user': user_profile.user, 'reviews': reviews})


def subscription_plan(request, subscription_id):
    all_subscriptions = SubscriptionPlan.objects.all()
    print(all_subscriptions)
    subscription = get_object_or_404(SubscriptionPlan, pk=subscription_id)
    movies = subscription.movies.all()
    return render(request, 'streaming/subscription_plan.html', {'subscription': subscription, 'movies': movies})
