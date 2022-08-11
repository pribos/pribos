from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import TaskSerializer, TagSerializer
from .models import Task, Tag
from django.db.models import Q
from datetime import date
from djmoney.money import Money
User = get_user_model()
today = date.today()
# Create your views here.


@api_view(['GET'])
def gettasks(request):
    # user = request.user

    user = User.objects.get(pkid=2)
    print("유저", user)
    # 검색어
    # keyword = request.query_params.getlist('keyword', None)
    
    # 필터링
    q = Q()
    tasks = Task.objects.all()

    q &= Q(user=user)

    tasks = tasks.distinct().filter(
        q
    )

    print("TASKS", tasks)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# 게시물 작성
@api_view(['POST'])
def posttask(request):
    data = request.data
    user = User.objects.get(pkid=3)
    # user = request.user
    print("POST REQUEST", request)
    print("POSTDATA", data)
    print("POSTUSER", user)

    print("POST MONEY", data['income_money'], data['income_currency'])

    print(Money(data['income_money'], data['income_currency']))
    print(data['expected_pay_day'])

    task = Task(
        user=user,
        title=data['title'],
        country=data['country'],
        income=Money(data['income_money'], data['income_currency']),
        expected_pay_day=data['expected_pay_day'],
        deadline=data['deadline'],
        client=data['client'],
        agency=data['agency'],
    )
    task.save()

    print("SAVED", task)
    serializer = TaskSerializer(task, many=False)

    return Response({'post': serializer.data}, status=200)


# 게시물 수정
@api_view(['PATCH'])
def edittask(request, pk):
    data = request.data
    user = request.user

    print(data['income_money'], data['income_currency'])

    try:
        task = task.objects.get(user=user, id=pk)

        task.title = data['title']
        task.income = data['income']
        task.country = data['country']
        task.expected_pay_day = data['expected_pay_day']
        task.actual_pay_day = data['actual_pay_day']
        task.deadline = data['deadline']
        task.submit_day = data['submit_day']
        task.client = data['client']
        task.agency = data['agency']
        task.salary = Money(data['income_money'], data['income_currency'])
        task.updated = datetime.now()

        task.save()

        serializer = TaskSerializer(task, many=False)

        return Response({'post': serializer.data, 'message': "EDITED"})
    except:
        return Response({'message': "UNAUTHORIZED"})


# 게시물 활성화 > 비활성화
@api_view(['PATCH'])
def deactivatetask(request, pk):

    try:
        task = task.objects.get(id=pk)

        task.visible = False
        task.save()
        serializer = TaskSerializer(task, many=False)

        return Response({'post': serializer.data, 'message': "DEACTIVATED"})
    except:
        return Response({'message': "FAILED"})


# 게시물 비활성화 > 활성화
@api_view(['PATCH'])
def activatetask(request, pk):

    try:
        task = task.objects.get(id=pk)

        task.created = datetime.now()
        task.visible = True
        task.save()
        serializer = TaskSerializer(task, many=False)

        return Response({'post': serializer.data, 'message': "ACTIVATED"})
    except:
        return Response({'message': "FAILED"})


# 태그 작성
@api_view(['POST'])
def posttag(request):
    data = request.data

    tag = Tag(
        name=data['name'],
    )
    tag.save()

    serializer = TagSerializer(tag, many=False)

    return Response({'post': serializer.data}, status=200)


# 태그 수정
@api_view(['PATCH'])
def edittag(request, pk):
    data = request.data
    user = request.user

    try:
        tag = Tag.objects.get(user=user, id=pk)

        tag.title = data['title']
        tag.updated = datetime.now()

        tag.save()

        serializer = TagSerializer(tag, many=False)

        return Response({'post': serializer.data, 'message': "EDITED"})
    except:
        return Response({'message': "UNAUTHORIZED"})
