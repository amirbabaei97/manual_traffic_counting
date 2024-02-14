from django.shortcuts import render
from django.urls import include, path
from django.http import JsonResponse
from .models import CarCount
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count as DjangoCount
from .models import CarType, CountingSession, CarCount
from django.utils import timezone

def start_session(request):
    if request.method == 'POST':
        session_name = request.POST.get('name')
        direction = request.POST.get('direction')
        
        if not session_name:
            messages.error(request, "Session name is required.")
            return render(request, 'start_session.html')
        
        if not direction:
            messages.error(request, "Direction is required.")
            return render(request, 'start_session.html')

        # Create session with current timestamp as start_time and an undefined end_time
        session = CountingSession.objects.create(
            name=session_name,
            direction=direction,
            start_time=timezone.now(),
        )
        return redirect('count_cars', session_id=session.id)
    else:
        return render(request, 'start_session.html')

def count_cars(request, session_id):
    session = CountingSession.objects.get(id=session_id)
    car_types = CarType.objects.all()

    # Calculate current counts for each car type in this session
    current_counts = CarCount.objects.filter(session=session) \
        .values('car_type__name') \
        .annotate(total=DjangoCount('id')) \
        .order_by('car_type__name')

    # Convert the QuerySet to a dictionary: {car_type_id: count, ...}
    counts_dict = {count['car_type__name']: count['total'] for count in current_counts}

    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'end_session':
            # Update the session's end_time
            session.end_time = timezone.now()
            session.save()
            # Redirect to start a new session
            return redirect('start_session')
        else:
            car_type_id = request.POST.get('car_type_id')
            car_type = CarType.objects.get(id=car_type_id)
            CarCount.objects.create(
                car_type=car_type,
                session=session,
                timestamp=timezone.now()
            )
            # Refresh the page with updated counts
            return redirect('count_cars', session_id=session.id)
    else:
        # Pass the counts dictionary to the template
        return render(request, 'count_cars.html', {'car_types': car_types, 'session_id': session.id, 'current_counts': counts_dict})
