# Landslide-WebGIS API

FastAPI cung cấp 11 GET endpoint dưới `/api/v1` cho M2. Dữ liệu phát triển đến từ PostgreSQL/PostGIS. Xem [schema, cách tạo DB và nạp seed](../database/README.md) và [hợp đồng API](../docs/api_specification.md).

## 1. Cài môi trường

Từ thư mục `backend/` trên Windows, tạo venv với Python 3.11 rồi cài thư viện. Ví dụ khi Python Launcher nhận diện được 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu dùng uv, lệnh tương đương là `uv venv --python 3.11 --seed .venv`, sau đó chạy cùng lệnh pip ở trên. Tạo `.env` từ `.env.example` nếu chưa có. `DATABASE_URL` dùng role đọc, `MIGRATION_DATABASE_URL` dùng role sở hữu, `TEST_DATABASE_URL` trỏ DB kiểm thử riêng. Biến môi trường của process được ưu tiên hơn file. File env phát triển nằm ngoài Git. Hoàn thành các bước tạo DB, migration và seed trong database README trước khi gọi API.

## 2. Chạy API và kiểm tra

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Từ một terminal khác:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/health'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/study-areas?area_type=province'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/rainfall?data_type=observation'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/alerts/-1'
```

Health trả `{"status":"ok","database":"connected"}` khi truy vấn DB thành công. Swagger UI tại [localhost/docs](http://127.0.0.1:8000/docs), ReDoc tại [localhost/redoc](http://127.0.0.1:8000/redoc), hợp đồng máy đọc được tại [localhost/openapi.json](http://127.0.0.1:8000/openapi.json).

## 3. Kiểm thử

Dựng và seed DB `landslide_webgis_test` theo phần 3 của database README. Từ `backend/` chạy:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m alembic check
```

Fixtures mở transaction và rollback trên DB kiểm thử, sử dụng bản ghi mẫu cố định. Pytest kiểm tra DB thật, 11 path trong OpenAPI, phân trang, lọc thời gian, lỗi 404/422/503 và chi tiết cảnh báo có các bản ghi mưa liên quan. `alembic check` dùng DB phát triển đã chạy migration, kết quả mong đợi là `No new upgrade operations detected.`

## 4. Cấu trúc

| Thư mục | Trách nhiệm |
|---|---|
| `app/core/` | Settings, SQLAlchemy engine và session |
| `app/models/` | ORM ánh xạ 10 bảng PostgreSQL/PostGIS |
| `app/schemas/` | Query, response, validation và phân trang |
| `app/repositories/` | Truy vấn, lọc và sắp xếp |
| `app/services/` | Tra tài nguyên và ghép chi tiết cảnh báo |
| `app/api/v1/endpoints/` | Router theo 7 nhóm tài nguyên |
| `migrations/`, `tests/` | Alembic và bộ kiểm thử |

`map-info` thuộc M3, cần metadata và dịch vụ bản đồ thực. Ingestion mưa và đánh giá cảnh báo thuộc M4. Dữ liệu demo M2 có nhãn riêng và bản đồ ở trạng thái draft.
