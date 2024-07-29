from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Records
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from .serializers import UserSerializer, BmiSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_user(request):
    """ Get User details """
    user = request.user
    serializer = UserSerializer(user)
    return Response({
        'user': serializer.data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def create_bmi(request):
    """ Calculate user bmi and save it """
    user = request.user
    try:
        height = request.data['height']
        weight = request.data['weight']
    except Exception as e:
        Response({'Error': e})
    bmi = float(weight) / (float(height) * float(height))
    bmi = round(bmi, 2)
    age = datetime.now().year - user.date_of_birth.year
    if datetime.now().month > user.date_of_birth.month:
        age += 1
    if bmi < 18.5:
        Classification = 'Underweight'
    elif bmi < 24.9:
        Classification = 'Normal Weight'
    elif bmi < 29.9:
        Classification = 'Overweight'
    else:
        Classification = 'Obese'

    try:
        record = Records.objects.create(
            weight=weight,
            height=height,
            bmi=bmi,
            Classification=Classification,
            user_id=user
        )
        return Response({'Your BMI is': record.bmi, 'Classification': Classification})
    except Exception as e:
        return Response({'Error': e})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_bmi(request):
    """ Get all saved bmi for a User """
    try:
        user = request.user
        QuerySet = Records.objects.filter(user_id=user).values().all()
        serializer = BmiSerializer(QuerySet, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'Error': e})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def user_delete(request):
    """ Remove user from database """
    try:
        user = request.user
        user.delete()
        return Response({'Deletion user': user.username})
    except Exception as e:
        return Response({'Error': e})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def user_update(request):
    """ Update user information """
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response('Error')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def delete_bmi(request):
    """ Remove BMI from database by id """
    user = request.user
    bmi_id = request.data.get('id')
    try:
        bmi_record = Records.objects.get(id=bmi_id, user_id=user)
        bmi_record.delete()
        return Response({'message': 'BMI record deleted successfully'}, status=status.HTTP_200_OK)
    except Records.DoesNotExist:
        return Response({'error': 'BMI record not found'}, status=status.HTTP_404_NOT_FOUND)