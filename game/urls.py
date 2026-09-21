from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/games", views.start_game, name="start-game"),
    path("api/games/<str:game_id>/guesses", views.send_guess, name="send-guess"),
    path("api/games/<str:game_id>", views.get_game, name="get-game"),
]
