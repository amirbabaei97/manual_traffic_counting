from django.shortcuts import render
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
    # Define the stream numbers range here for reuse
    stream_numbers = range(1, 13)
    
    if request.method == 'POST':
        session_name = request.POST.get('name')
        direction = request.POST.get('direction')
        streams = request.POST.getlist('streams')  # Get list of selected streams
        
        if not session_name or not direction or not streams:
            # Use Django's messages framework for error handling
            if not session_name:
                messages.error(request, "Session name is required.")
            if not direction:
                messages.error(request, "Direction is required.")
            if not streams:
                messages.error(request, "At least one stream is required.")
            
            # Repass necessary context for the template to render properly again
            return render(request, 'start_session.html', {'stream_numbers': stream_numbers})
        
        # Proceed with creating the session
        streams_str = ','.join(streams)  # Join the list of streams into a comma-separated string
        session = CountingSession.objects.create(
            name=session_name,
            direction=direction,
            start_time=timezone.now(),
            streams=streams_str,
        )
        return redirect('count_cars', session_id=session.id)
    else:
        # Pass the streams range to the template on GET requests
        return render(request, 'start_session.html', {'stream_numbers': stream_numbers})

@login_required
def count_cars(request, session_id):
    session = CountingSession.objects.get(id=session_id)
    car_types = CarType.objects.all()
    selected_streams = list(map(int, session.streams.split(','))) if session.streams else []

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
        if 'action' in request.POST and request.POST['action'] == 'end_session':
            session.end_time = timezone.now()
            session.save()
            return redirect('start_session')
        else:
            car_type_id = request.POST.get('car_type_id')
            # Here, you'd also need to know which stream the count is for
            # This information could come from an additional input in your form
            stream_number = request.POST.get('stream_number')
            car_type = CarType.objects.get(id=car_type_id)
            CarCount.objects.create(
                car_type=car_type,
                session=session,
                timestamp=timezone.now(),
                stream_number=stream_number  # Assuming this field exists
            )
            return redirect('count_cars', session_id=session.id)
    else:
        return render(request, 'count_cars.html', {
            'car_types': car_types,
            'session_id': session.id,
            'current_counts': counts_dict,
            'stream_counts': stream_dict,
            'selected_streams': selected_streams
        })