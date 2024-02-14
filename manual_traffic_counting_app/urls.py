from django.urls import path
from .views import start_session, count_cars  

urlpatterns = [
    path('start-session/', start_session, name='start_session'),
    path('count-cars/<int:session_id>/', count_cars, name='count_cars'),
]
