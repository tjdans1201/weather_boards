from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Board
from .serializers import BoardSerializer, BoardDetailSerailizer, BoardCreateSerailizer
from rest_framework.generics import get_object_or_404
import requests
import json
import re
from argon2 import PasswordHasher

# Create your views here.


@api_view(["GET"])
def get_board_list(request):
    """
    모든 게시판 정보를 리턴한다.
    """
    boards = Board.objects.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_board_detail(request, id):
    """
    지정된 ID를 가진 게시물 정보를 리턴한다.
    """
    board = get_object_or_404(Board, id=id)
    serializer = BoardDetailSerailizer(board)
    return Response(serializer.data, status=status.HTTP_200_OK)

    
def check_password(password):
    """
    패스워드 적합성 체크
    """    
    flg = False
    message = ""
    if len(password) < 6:
        message = "비밀번호는 최소 6자 이상입니다."
        return flg, message
    elif not re.findall("[0-9]", password):
        message = "비밀번호는 최소 1개 이상의 숫자가 필요합니다"
        return flg, message
    flg = True
    return flg,message

@api_view(["POST"])
def create_board(request):
    """
    게시물을 작성한다.
    데이터 생성 시 현재 날씨를 외부 API로부터 취득하여 추가한다.
    """
    try:
        request_body = request.data
        pwd_validation, message = check_password(request.data["password"])
        # 패스워드 validation 체크
        if pwd_validation == False:
            return Response({"message":message}, status=status.HTTP_400_BAD_REQUEST)
        request_body["password"] = PasswordHasher().hash(request_body["password"])
        # 현재 날씨 취득
        response = requests.get(url = "http://api.weatherapi.com/v1/current.json?key=958993396adc4c6ea8701154220609&q=seoul&aqi=no&lang=ko")
        response_body = json.loads(response.content)
        weather_condition = response_body["current"]["condition"]["text"]
        request_body["current_weather"] = weather_condition
        serializer = BoardCreateSerailizer(data=request_body)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"success"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def delete_board(request, id):
    """
    게시물을 삭제한다.
    입력받은 password와 게시물의 password가 동일하면 삭제한다.

    """
    try:
        password = request.data["password"]
        board = get_object_or_404(Board, id=id)
        # 패스워드  체크
        try:
            PasswordHasher().verify(board.password, password)
        except Exception as e:
            return Response({"message":"패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 삭제
        board.delete()
        return Response({"message":"success"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

