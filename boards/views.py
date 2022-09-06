from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Board
from .serializers import BoardSerializer, BoardDetailSerailizer
from rest_framework.generics import get_object_or_404

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
