from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, BoardCreateSerializer, BoardUpdateSerializer
from rest_framework.generics import get_object_or_404
import requests
import json
import re
from argon2 import PasswordHasher

# Create your views here.


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
    return flg, message


def check_title_content(title, content):
    """
    제목, 본문 적합성 체크
    """
    flg = False
    message = ""
    if len(title) > 20:
        message = "제목은 최대 20자입니다."
        return flg, message
    elif len(content) > 200:
        message = "본문은 최대 200자입니다."
        return flg, message
    flg = True
    return flg, message


class BoardsAPI(APIView):
    def get(self, request):
        """
        모든 게시판 정보를 리턴한다.
        페이지네이션 구현, 1 page당 count 20
        """
        try:
            # page 번호 체크
            page = int(request.query_params["page"])
            count = 20
            offset = int((count*(page-1)))
            boards = Board.objects.all().order_by("created_at")[offset:offset+count]
            serializer = BoardSerializer(boards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        게시물을 작성한다.
        데이터 생성 시 현재 날씨를 외부 API로부터 취득하여 추가한다.
        """
        try:
            request_body = request.data
            title_content_validation, message = check_title_content(
                request.data["title"], request.data["content"]
            )
            # 제목, 본론 validation 체크
            if title_content_validation == False:
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
            pwd_validation, message = check_password(request.data["password"])
            # 패스워드 validation 체크
            if pwd_validation == False:
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
            # 패스워드 암호화
            request_body["password"] = PasswordHasher().hash(request_body["password"])
            # 현재 날씨 취득 (한국 서울 기준)
            # ※ 날씨 정보 취득에 필요한 API Key 입력필요
            weather_api_key = ""
            response = requests.get(
                url="http://api.weatherapi.com/v1/current.json?key="+str(weather_api_key)+"&q=seoul&aqi=no&lang=ko"
            )
            response_body = json.loads(response.content)
            weather_condition = response_body["current"]["condition"]["text"]
            request_body["current_weather"] = weather_condition
            serializer = BoardCreateSerializer(data=request_body)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "게시물이 등록되었습니다."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BoardAPI(APIView):
    def get(self, request, id):
        """
        지정된 ID를 가진 게시물 정보를 리턴한다.
        """
        try:
            board = get_object_or_404(Board, id=id)
            serializer = BoardDetailSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, id):
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
            except Exception:
                return Response(
                    {"message": "패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
                )
            # 삭제
            board.delete()
            return Response({"message": "게시물이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, id):
        """
        게시물을 수정한다.
        입력받은 패스워드가 기존 패스워드와 같으면 수정 가능.
        """        
        try:
            request_body = request.data
            board = get_object_or_404(Board, id=id)
            # 패스워드 체크
            try:
                PasswordHasher().verify(board.password, request.data["password"])
            except Exception:
                return Response(
                    {"message": "패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
                )
            # 제목, 본론 validation 체크
            title = request_body["title"]
            content = request_body["content"]
            title_content_validation, message = check_title_content(title, content)
            if title_content_validation == False:
                 return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
            # # 해당 게시물 update
            serializer = BoardUpdateSerializer(board, data=request_body)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"게시물이 수정되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
