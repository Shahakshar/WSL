from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[openapi.Parameter('email', openapi.IN_PATH, description="User email", type=openapi.TYPE_STRING)],
    responses={200: UserSerializer}
)
@swagger_auto_schema(
    method='put',
    request_body=UserSerializer,
    responses={200: UserSerializer}
)
@swagger_auto_schema(
    method='delete',
    manual_parameters=[openapi.Parameter('email', openapi.IN_PATH, description="User email", type=openapi.TYPE_STRING)],
    responses={204: 'User deleted successfully'}
)
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, email):
    user = get_object_or_404(User, email=email)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def get_user_by_email(request, email):
#     user = get_object_or_404(User, email=email)
#     serializer = UserSerializer(user)
#     return Response(serializer.data)

# @api_view(['PUT'])
# def update_user(request, email):
#     user = get_object_or_404(User, email=email)
#     serializer = UserSerializer(user, data=request.data, partial=True)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def delete_user(request, email):
#     user = get_object_or_404(User, email=email)
#     user.delete()
#     return Response({'message': 'User deleted Successfully.'},status=status.HTTP_204_NO_CONTENT)
