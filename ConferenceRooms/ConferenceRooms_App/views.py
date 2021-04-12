from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views import View
from ConferenceRooms_app.models import Room


class Overview(View):
    # Gives you an overview of all the rooms available for booking.

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        if not rooms:
            messages.info(request, "No rooms to show")
        return render(request, template_name='all_rooms.html', context={'rooms': rooms})


class RoomDetails(View):
    # Detailed view of chosen room. Shows name, capacity, booking etc.

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, template_name='room_details.html', context={'room': room})


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
        projector_yes = request.POST.get('projectorY')
        projector_no = request.POST.get('projectorN')
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

        if projector_yes:
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
        projector_yes = request.POST.get('projectorY')
        room = Room.objects.get(id=room_id)

        if not name:
            alert_message = 'Please add a name for the room.'
            return render(request, template_name='modify_room.html',
                          context={'alert_message': alert_message})

        if capacity <= 0:
            alert_message = 'Number of seats must be more than 0!'
            return render(request, template_name='modify_room.html',
                          context={'alert_message': alert_message})

        if projector_yes:
            room.projector = True
        else:
            room.projector = False

        room.name = name
        room.capacity = capacity
        room.save()
        messages.success(request, 'The room has been modified.')
        return redirect('all_rooms')
