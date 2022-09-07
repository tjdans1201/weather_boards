# wheather_boards
----------
## 개발기간
#### 2022-09-06 ~ 2022-09-07

## 프로젝트 설명
 - 로그인 없이 작성, 수정, 삭제, 조회가 가능한 게시판 기능을 제공하는 서버 개발
 - 게시글 작성 시 현재 날씨를 기록
 
## 사용된 기술
 - **Back-End** : Python, Django, Django REST framework
 
## ERD
<img width="196" alt="erd" src="https://user-images.githubusercontent.com/57758265/188793205-90f0d67d-0ab9-40c9-a9a8-db76d2c853ef.png">

## API_DOCS

### 게시물 리스트 조회
- 최근 작성된 게시물부터 리스트를 리턴한다.
- page 당 20개의 게시물에 대한 정보를 리턴한다.

API URL

GET api/boards?page=<int>

#### Response_body
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|게시글 리스트|board_list|dictionary[]||
|id|id|int||
|작성자|author|str||
|제목|title|str||
|본문|content|str||
|작성 시간|created_at|str||
|날씨|current_weather|str||
|수정 시간|updated_at|str||

#### HTTP status code
| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상종료 |
| 500 | Internal Server Error | 서버 에러가 발생하였습니다. | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "board_list": [
        {
            "id": 47,
            "title": "titledddddddd",
            "content": "helllllllllsss",
            "author": "aaaaaaa",
            "created_at": "2022-09-07T11:02:39.652610",
            "current_weather": "맑음",
            "updated_at": "2022-09-07T11:02:39.652610"
        },
        {
            "id": 46,
            "title": "title",
            "content": "hello",
            "author": "aaaaaaa",
            "created_at": "2022-09-07T11:02:39.652610",
            "current_weather": "맑음",
            "updated_at": "2022-09-07T11:02:39.652610"
        }
	]
}
```

2) 500

```json
{
    "Message": "서버 에러가 발생하였습니다."
}
```
### 게시물 상세 조회

API URL

GET api/boards/<int:id>

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|게시글|board_data|dictionary||
| id | id | int |  |
| 작성자 | author | str |  |
| 제목 | title | str |  |
| 본문 | content | str |  |
| 현재 날씨 | currnet_weather | str |  |
| 작성 시간 | created_at | str |  |
| 수정 시간 | updated_at | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상 |
| 500 | Internal Server Error | Exception 메시지 | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "board_data": 
        {
            "id": 47,
            "title": "titledddddddd",
            "content": "helllllllllsss",
            "author": "aaaaaaa",
            "created_at": "2022-09-07T11:02:39.652610",
            "current_weather": "맑음",
            "updated_at": "2022-09-07T11:02:39.652610"
        } 
}
```

2) 500

```json
{
    "message": "서버 에러가 발생하였습니다"
}
```


### 게시물 등록
- 게시물을 등록한다.
- password는 6자 이상이며 숫자가 포함되어있어야한다.
- password는 암호화해서 저장한다.
- 제목과 본문은 각각 20자, 200자 이내로 제한한다.
- 외부 API로부터 현재날씨를 받아서 저장한다.

API URL

POST api/boards

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 작성자 | author | str |  |
| 제목 | title | str | 20자 이내 제한 |
| 본문 | content | str | 200자 이내 제한 |
| 비밀번호 | password | str | 6자 이상이며 숫자 포함 필수 |

Request Example

```json
{"author":"kim","title":"title", "content":"hello", "password":"password1"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | 게시물이 등록되었습니다. | 정상종료 |
| 400 | Request Error | "비밀번호는 최소 6자 이상입니다.”,"비밀번호는 최소 1개 이상의 숫자가 필요합니다”,"제목은 최대 20자입니다.”,"본문은 최대 200자입니다.” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "success"
}
```

2) 400

```json
{
    "message": "제목은 최대 20자입니다."
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

### 게시물 수정
- Request Body의 password와 해당 게시물의 password가 같으면 제목과 본문을 수정할 수 있다.

API URL

PUT api/boards/<int:id>

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| password | password | str |  |
| 제목 | title | str | 20자 이내로 제한 |
| 본문 | content | str | 200자 이내로 제한 |

Request Example

```json
{"password":"password1", "title":"new_title","content":"new_content"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | “게시물이 수정되었습니다.” | 정상종료 |
| 400 | Request Error | "비밀번호가 틀렸습니다.”,"제목은 최대 20자입니다.”,"본문은 최대 200자입니다.” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "게시물이 수정되었습니다."
}
```

2) 400

```json
{
    "message": "비밀번호가 틀렸습니다."
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

### 게시물 삭제
- request_body의 비밀번호와 해당 게시물의 비밀번호가 같으면 게시물을 삭제한다.

API URL

Delete api/boards/<int:id>

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 비밀번호 | password | str |  |

Request Example

```json
{"password":"password1"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | “게시물이 삭제되었습니다.” | 정상종료 |
| 400 | Request Error | "비밀번호가 틀렸습니다.” | Request_body  문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "게시물이 삭제되었습니다."
}
```

2) 400

```json
{
    "message": "비밀번호가 틀렸습니다."
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```
## Unit test
- 각 method에 대해 유닛테스트 실행
<img width="324" alt="test_list" src="https://user-images.githubusercontent.com/57758265/188797526-543d9d4f-4c17-47e4-bd1f-7017c7b0ed3d.png">
<img width="461" alt="화면 캡처 2022-09-07 144024" src="https://user-images.githubusercontent.com/57758265/188797534-8d1c950e-892a-406d-98f6-8631529dc4ed.png">



