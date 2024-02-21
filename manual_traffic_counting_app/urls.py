from django.urls import path
from .views import start_session, count_cars , UserLoginView, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('start-session/', start_session, name='start_session'),
    path('count-cars/<int:session_id>/', count_cars, name='count_cars'),
]
