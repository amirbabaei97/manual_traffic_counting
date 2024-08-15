from django.shortcuts import render, get_object_or_404
from .models import CarCount
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count as DjangoCount
from .models import CarType, CountingSession, CarCount
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

class UserLoginView(LoginView):
    template_name = 'login.html'  # Path to your login template
    redirect_authenticated_user = True
    next_page = reverse_lazy('start_session')  # Redirect to home page upon login

@login_required
def start_session(request):
    car_types = CarType.objects.all()  # Get all car types to display in the form
    stream_numbers = range(1, 13)
    
    if request.method == 'POST':
        session_name = request.POST.get('name')
        direction = request.POST.get('direction')
        streams = request.POST.getlist('streams')
        selected_car_type_ids = request.POST.getlist('car_types')  # Get list of selected car types
        
        if not session_name or not direction or not streams or not selected_car_type_ids:
            messages.error(request, "All fields are required.")
            return render(request, 'start_session.html', {
                'stream_numbers': stream_numbers, 'car_types': car_types
            })
        
        streams_str = ','.join(streams)
        session = CountingSession.objects.create(
            name=session_name,
            direction=direction,
            start_time=timezone.now(),
            streams=streams_str,
        )
        session.car_types.set(selected_car_type_ids)  # Associate selected car types with the session
        return redirect('count_cars', session_id=session.id)
    else:
        return render(request, 'start_session.html', {
            'stream_numbers': stream_numbers, 'car_types': car_types
        })


@login_required
def count_cars(request, session_id):
    session = CountingSession.objects.get(id=session_id)
    car_types = session.car_types.all()
    selected_streams = list(map(int, session.streams.split(','))) if session.streams else []
    
    grid_positions = {
        1: "2 / 1", 2: "3 / 1", 3: "4 / 1",
        4: "5 / 2", 5: "5 / 3", 6: "5 / 4",
        7: "4 / 5", 8: "3 / 5", 9: "2 / 5",
        10: "1 / 2", 11: "1 / 3", 12: "1 / 4",
    }

    # Filter selected_streams to include only those with an associated grid position
    valid_streams = [stream for stream in selected_streams if stream in grid_positions]

    stream_dict = {}
    stream_counts = {}
    for stream in selected_streams:
        stream_counts[stream] = CarCount.objects.filter(session=session, stream_number=stream) \
            .values('car_type__name') \
            .annotate(total=DjangoCount('id')) \
            .order_by('car_type__name')

    for stream in stream_counts:
        stream_dict[stream] = {count['car_type__name']: count['total'] for count in stream_counts[stream]}

    current_counts = CarCount.objects.filter(session=session) \
        .values('car_type__name') \
        .annotate(total=DjangoCount('id')) \
        .order_by('car_type__name')

    counts_dict = {count['car_type__name']: count['total'] for count in current_counts}

    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'end_session':
                session.end_time = timezone.now()
                session.save()
                return redirect('start_session')
            elif request.POST['action'] == 'undo':
                # Handle the undo action
                car_count_id = request.POST.get('car_count_id')
                if car_count_id:
                    car_count = get_object_or_404(CarCount, id=car_count_id)
                    car_count.delete()
                    messages.success(request, 'Last action has been undone.')
                return redirect('count_cars', session_id=session.id)
        else:
            car_type_id = request.POST.get('car_type_id')
            stream_number = request.POST.get('stream_number')
            car_type = CarType.objects.get(id=car_type_id)
            CarCount.objects.create(
                car_type=car_type,
                session=session,
                timestamp=timezone.now(),
                stream_number=stream_number
            )
            return redirect('count_cars', session_id=session.id)

    # Get the last car count entry for undo
    last_car_count = CarCount.objects.filter(session=session).order_by('-timestamp').first()

    return render(request, 'count_cars.html', {
        'car_types': car_types,
        'session_id': session.id,
        'current_counts': counts_dict,
        'stream_counts': stream_dict,
        'selected_streams': valid_streams,  # Pass valid_streams instead
        'grid_positions': grid_positions,  # New
        'last_car_count': last_car_count,  # New context variable
    })
