from django.urls import path
from streaming.views import movie, index, user_reviews, subscription_plan, user_subscription

app_name = 'streaming'

urlpatterns = [
    path('', index, name='index'),
    path('movie/<int:movie_id>/', movie, name='movie'),
    path('user/<int:user_id>/', user_reviews, name='user_reviews'),
    path('subscriptionplan/<int:subscription_id>/', subscription_plan, name='subscription_plan'),
    path('user/subscription/', user_subscription, name='user_subscription'),

]
