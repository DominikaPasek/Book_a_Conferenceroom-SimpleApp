from django.db.models import Min
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views import View
from ConferenceRooms_app.models import Room, Booking
from datetime import date


class Overview(View):
    # Gives you an overview of all the rooms available for booking.

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        for room in rooms:
            booking_dates = [booking.date for booking in room.booking_set.all()]
            room.reserved = date.today() in booking_dates
        if not rooms:
            messages.info(request, "No rooms to show")
        return render(request, template_name='all_rooms.html', context={'rooms': rooms})

    def post(self, request):
        button_clicked = request.POST.get('search_button')
        if button_clicked:
            search = request.POST.get('search')
            if search == 'projector':
                rooms_with_projector = Room.objects.filter(projector="True")
                return render(request, template_name='search.html',
                              context={'rooms_with_projector': rooms_with_projector})
            else:
                rooms = Room.objects.filter(name__startswith=search)
                return render(request, template_name='search.html', context={'rooms': rooms})
                # search = int(search)
                # rooms = Room.objects.filter(capacity__gt=search)
                # return render(request, template_name='search.html', context={'rooms': rooms})


class RoomDetails(View):
    # Detailed view of chosen room. Shows name, capacity, booking etc.

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        bookings = Booking.objects.all().filter(room_id=room)
        return render(request, template_name='room_details.html', context={'room': room, 'bookings': bookings})


class AddNewRoom(View):
    # You can add a new room to the database,
    # while checking if a room of this name already exists in database and
    # checking if number of the seats is correct.

    def get(self, request):
        return render(request, template_name='add_new_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector')
        room = Room.objects.filter(name=name).first()

        if not name:
            alert_message = 'Please add a name for the room.'
            return render(request, template_name='add_new_room.html',
                          context={'alert_message': alert_message})
        if room:
            if room.name == name:
                alert_message = "There's a room with this name in our database already. " \
                                "Please choose another room name."
                return render(request, template_name='add_new_room.html',
                              context={'alert_message': alert_message})

        if capacity <= 0:
            alert_message = 'Number of seats must be more than 0!'
            return render(request, template_name='add_new_room.html',
                          context={'alert_message': alert_message})

        if projector == "True":
            Room.objects.create(name=name, capacity=capacity, projector=True)
        else:
            Room.objects.create(name=name, capacity=capacity, projector=False)

        messages.success(request, 'The room has been added to our database.')
        return redirect('all_rooms')


def delete_room(request):
    # Informs the user of what to do to delete a room.
    message = "Please put an id number of the room you wish to delete at the end of the URL."
    return render(request, template_name='empty.html', context={"message": message})


class DeleteRoom(View):
    # You can delete a room of your choosing by putting it's id number at the end of the url.

    def get(self, request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except (Room.DoesNotExist, AttributeError):
            message= "There is no room with this ID."
            return render(request, template_name='empty.html', context={'message': message})
        context = {'room': room}
        return render(request, template_name='delete_room.html', context=context)

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        messages.success(request, 'The room has been deleted from our database.')
        return redirect('all_rooms')


def modify_room(request):
    # Informs the user of what to do to get to modify view.
    message = "Please put an id number of the room you wish to modify at the end of the URL."
    return render(request, template_name='empty.html', context={"message": message})


class ModifyRoom(View):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except (Room.DoesNotExist, AttributeError):
            message = "There is no room with this ID."
            return render(request, template_name='empty.html', context={'message': message})
        context = {'room': room}
        return render(request, template_name='modify_room.html', context=context)

    def post(self, request, room_id):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector')
        room = Room.objects.get(id=room_id)

        if not name:
            alert_message = 'Please add a name for the room.'
            return render(request, template_name='modify_room.html',
                          context={'alert_message': alert_message})

        if capacity <= 0:
            alert_message = 'Number of seats must be more than 0!'
            return render(request, template_name='modify_room.html',
                          context={'alert_message': alert_message})

        if projector == "True":
            room.projector = True
        else:
            room.projector = False

        room.name = name
        room.capacity = capacity
        room.save()
        messages.success(request, 'The room has been modified.')
        return redirect('all_rooms')


class RoomBooking(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        bookings = Booking.objects.all().filter(room_id=room)
        return render(request, template_name='book_a_room.html', context={'room': room, 'bookings': bookings})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        date_wanted = request.POST.get('day')
        comment = request.POST.get('comment')

        available = Booking.objects.filter(room_id=room.id, date=str(date_wanted))

        if available:
            alert_message = "We are sorry, but this room is booked for that day. " \
                            "Please, choose another day/another room or contact us at 123 456 789."
            return render(request, template_name='book_a_room.html', context={'room': room, 'alert_message': alert_message})

        if date_wanted < str(date.today()):
            alert_message = "Wrong date!"
            return render(request, template_name='book_a_room.html', context={'alert_message': alert_message})
        else:
            Booking.objects.create(date=date_wanted, room_id=room, comment=comment if comment else None)
            messages.success(request, "Congratulations! The room has been booked.")
            return redirect('all_rooms')
