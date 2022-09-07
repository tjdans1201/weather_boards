from django.test import TestCase
from rest_framework.test import APIClient
from boards.models import Board
from datetime import datetime
from unittest import mock
import json
from argon2 import PasswordHasher
import os
import pandas as pd

curDir = os.path.dirname(os.path.normpath(__file__))

# 더미데이터 생성
def set_dummy():
    df = pd.read_csv(curDir + "/dummy/board_list.csv")
    dict_df = df.to_dict("records")
    boards = [
        Board(
            author=x["author"],
            title=x["title"],
            content=x["content"],
            current_weather=x["current_weather"],
        )
        for x in dict_df
    ]
    Board.objects.bulk_create(boards)


# 날씨 요청 mock
def call_weather_success(url, timeout=None, status_code=None):
    class MockResponse:
        def __init__(self, url, content, status_code):
            self.url = url
            self.content = content.encode()
            self.status_code = status_code

    return MockResponse(
        url,
        json.dumps(
            {
                "location": {
                    "name": "Seoul",
                    "region": "",
                    "country": "South Korea",
                    "lat": 37.57,
                    "lon": 127.0,
                    "tz_id": "Asia/Seoul",
                    "localtime_epoch": 1662512292,
                    "localtime": "2022-09-07 9:58",
                },
                "current": {
                    "last_updated_epoch": 1662511500,
                    "last_updated": "2022-09-07 09:45",
                    "temp_c": 19.7,
                    "temp_f": 67.5,
                    "is_day": 1,
                    "condition": {
                        "text": "맑음",
                        "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                        "code": 1000,
                    },
                    "wind_mph": 2.2,
                    "wind_kph": 3.6,
                    "wind_degree": 93,
                    "wind_dir": "E",
                    "pressure_mb": 1017.0,
                    "pressure_in": 30.02,
                    "precip_mm": 0.0,
                    "precip_in": 0.0,
                    "humidity": 73,
                    "cloud": 0,
                    "feelslike_c": 19.7,
                    "feelslike_f": 67.5,
                    "vis_km": 10.0,
                    "vis_miles": 6.0,
                    "uv": 5.0,
                    "gust_mph": 1.6,
                    "gust_kph": 2.5,
                },
            }
        ),
        200,
    )
"""
views.py unittest

1. test_create
    1) 실패(패스워드가 6자 미만인 경우)
    2) 실패(패스워드에 숫자가 없는 경우)
    3) 실패(제목이 20자 초과하는 경우)
    4) 실패(본문이 200자 초과하는 경우)
    5) 성공

2. test_board_detail
    1) 성공

3. test_board_update
    1) 실패(비밀번호가 틀렸을 경우)
    2) 실패(제목이 20자를 초과하는 경우)
    3) 실패(본문이 200자를 초과하는 경우)
    4) 성공

4. test_board_delete
    1) 실패(비밀번호가 틀렸을 경우)
    2) 성공

5. test_get_board_list
    # data 40개 존재
    1) 성공(1페이지) 20개 리턴
    2) 성공(2페이지) 20개 리턴
    3) 성공(3페이지) 0개 리턴
"""


class TestViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        pass

    @mock.patch("requests.get", side_effect=call_weather_success)
    def test_create(self, mock_get):
        # 게시물 등록 테스트
        print("-----------------------------------------")
        print("start_test_create")
        client = APIClient()
        # case_1 : 실패(패스워드가 6자 미만인 경우)
        result = client.post(
            "/api/boards",
            {
                "author": "tester",
                "title": "test",
                "content": "testing",
                "password": "test1",
            },
            format="json",
        )
        exp = {"message": "비밀번호는 최소 6자 이상입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

        # case_2 : 실패(패스워드에 숫자가 없는 경우)
        result = client.post(
            "/api/boards",
            {
                "author": "tester",
                "title": "test",
                "content": "testing",
                "password": "testaaa",
            },
            format="json",
        )
        exp = {"message": "비밀번호는 최소 1개 이상의 숫자가 필요합니다"}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)
        print("finish_test_create")

        # case_3 : 실패(제목이 20자 초과하는 경우)
        result = client.post(
            "/api/boards",
            {
                "author": "tester",
                "title": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "content": "testing",
                "password": "testaaa",
            },
            format="json",
        )
        exp = {"message": "제목은 최대 20자입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)
        print("finish_test_create")

        # case_4 : 실패(본문이 200자 초과하는 경우)
        result = client.post(
            "/api/boards",
            {
                "author": "tester",
                "title": "test",
                "content": "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789",
                "password": "testaaa1",
            },
            format="json",
        )
        exp = {"message": "본문은 최대 200자입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)
        print("finish_test_create")

        # case_5 : 성공
        param = {
            "author": "tester",
            "title": "test1",
            "content": "testing",
            "password": "test01",
        }
        result = client.post(
            "/api/boards",
            param,
            format="json",
        )
        exp = {"message": "게시물이 등록되었습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.data, exp)
        registered_data = Board.objects.get(title="test1")
        print({"registered_data": registered_data.id})
        self.assertEqual(registered_data.author, param["author"])
        self.assertEqual(registered_data.title, param["title"])
        self.assertEqual(registered_data.content, param["content"])
        print("finish_test_create")
        print("-----------------------------------------")

    def test_board_detail(self):
        # 게시물 상세 취득 테스트
        print("-----------------------------------------")
        print("start_test_board_detail")
        Board.objects.create(
            title="test_board_detail",
            content="test_board_detail_content",
            author="tester",
            current_weather="맑음",
        )
        client = APIClient()
        # case_1 : 성공
        response = client.get("/api/boards/1")
        result = response.data
        self.assertEqual(result["title"], "test_board_detail")
        self.assertEqual(result["content"], "test_board_detail_content")
        self.assertEqual(result["author"], "tester")
        self.assertEqual(result["current_weather"], "맑음")
        print("finish_test_board_detail")
        print("-----------------------------------------")

    def test_board_update(self):
        # 게시물 수정 테스트
        print("-----------------------------")
        print("finish_test_board_update")
        client = APIClient()
        Board.objects.create(
            title="test_board_update_1",
            content="test_board_update_content_1",
            author="tester",
            current_weather="맑음",
            password=PasswordHasher().hash("test01"),
        )

        # case_1 실패(비밀번호가 틀렸을 경우)
        result = client.put(
            "/api/boards/1",
            {
                "title": "test_board_update_2",
                "content": "test_board_update_content_2",
                "password": "testaaa1",
            },
            format="json",
        )
        exp = {"message": "패스워드가 틀렸습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

        # case_2 실패(제목이 20자를 초과하는 경우)
        result = client.put(
            "/api/boards/1",
            {
                "title": "test_board_update_2222222222222",
                "content": "test_board_update_content_2",
                "password": "test01",
            },
            format="json",
        )
        exp = {"message": "제목은 최대 20자입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)
        print("finish_test_board_update")
        print("-----------------------------")

        # case_3 실패(본문이 200자를 초과하는 경우)
        result = client.put(
            "/api/boards/1",
            {
                "title": "test_board_update_2",
                "content": "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789",
                "password": "test01",
            },
            format="json",
        )
        exp = {"message": "본문은 최대 200자입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)
        print("finish_test_board_update")
        print("-----------------------------")

        # case_4 성공
        result = client.put(
            "/api/boards/1",
            {
                "title": "test_board_update_2",
                "content": "test_board_update_content_2",
                "password": "test01",
            },
            format="json",
        )
        exp = {"message": "게시물이 수정되었습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, exp)
        updated_data = Board.objects.get(id=1)
        self.assertEqual(updated_data.title, "test_board_update_2")
        self.assertEqual(updated_data.content, "test_board_update_content_2")
        print("finish_test_board_update")
        print("-----------------------------")

    def test_board_delete(self):
        # 게시물 삭제 테스트
        print("-----------------------------")
        print("start_test_board_delete")
        client = APIClient()
        Board.objects.create(
            title="test_board_delete",
            content="test_board_delete_content",
            author="tester",
            current_weather="흐림",
            password=PasswordHasher().hash("test01"),
        )
        test_data_1 = Board.objects.all()
        print(test_data_1)
        self.assertEqual(len(test_data_1), 1)

        # case_1 실패(비밀번호가 틀렸을 경우)
        result = client.delete(
            "/api/boards/1",
            {"password": "testaaa1"},
            format="json",
        )
        exp = {"message": "패스워드가 틀렸습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

        # case_2 성공
        result = client.delete(
            "/api/boards/1",
            {"password": "test01"},
            format="json",
        )
        exp = {"message": "게시물이 삭제되었습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, exp)
        test_data_2 = Board.objects.all()
        print({"test_data_2": test_data_2})
        self.assertEqual(len(test_data_2), 0)

        print("finish_test_board_delete")
        print("-----------------------------")

    def test_get_board_list(self):
        # 게시물 리스트 취득 테스트(페이지네이션)
        print("-----------------------------------------")
        print("start_test_get_board_list")
        set_dummy()
        client = APIClient()
        board_list = Board.objects.all()
        print({"board_list": board_list.values()})
        print({"len(board_list)": len(board_list)})
        # board table(data 40개 존재)
        # case_1 : 성공(1페이지) 20개 리턴
        response = client.get("/api/boards?page=1")
        result = response.data
        print(result)
        self.assertEqual(len(result), 20)

        # case_2 : 성공(2페이지) 20개 리턴
        response = client.get("/api/boards?page=2")
        result = response.data
        print(result)
        self.assertEqual(len(result), 20)

        # case_2 : 성공(3페이지) 0개 리턴
        response = client.get("/api/boards?page=3")
        result = response.data
        print(result)
        self.assertEqual(len(result), 0)
        print("finish_test_get_board_list")
        print("-----------------------------------------")
