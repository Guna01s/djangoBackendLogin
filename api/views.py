from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import mysql.connector as sql
from .models import Users


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not name or not email or not password:
        return Response({'error': 'Please provide a name, email, and password.', 'status_code': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists in the database
    db = sql.connect(host="localhost", user="root", passwd="root", database='users_database_api')
    cursor = db.cursor()

    check_query = "SELECT * FROM users_database_api WHERE email = %s"
    cursor.execute(check_query, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        db.close()
        return Response({'error': 'Email already exists. Please choose a different email.', 'status_code': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Insert user data into the 'users_database_api' table
    insert_query = "INSERT INTO users_database_api (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)
    cursor.execute(insert_query, values)

    db.commit()
    db.close()

    return Response({'message': 'User registered successfully.', 'status_code': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Connect to the MySQL database
    db = sql.connect(host="localhost", user="root", passwd="root", database='users_database_api')
    cursor = db.cursor()

    # Execute a query to retrieve user data
    select_query = "SELECT * FROM users_database_api WHERE email=%s AND password=%s"
    values = (email, password)
    cursor.execute(select_query, [email,password])

    result = cursor.fetchall()

    db.close()

    # for checking result
    if result:
        return Response({'message': 'Login successful.', 'status_code': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.', 'status_code': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
