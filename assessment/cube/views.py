from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cube.models import EndUser, EndUserEvent
from cube.serializers import EndUserEventSerializer


@api_view(['GET', 'POST'])
def end_user_event_list(request):
    """
    List all end user events, or create a new end user event.
    """
    if request.method == 'GET':
        events = EndUserEvent.objects.all()
        serializer = EndUserEventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = EndUser.objects.create(user_id=str(request.data["user"]))
        serializer = EndUserEventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)