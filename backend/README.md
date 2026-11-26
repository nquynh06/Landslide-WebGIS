# Landslide-WebGIS API

FastAPI cung cấp 11 GET endpoint dưới `/api/v1` cho M2. Dữ liệu phát triển đến từ PostgreSQL/PostGIS. Xem [schema, cách tạo DB và nạp seed](../database/README.md) và [hợp đồng API](../docs/api_specification.md).

## 1. Cài môi trường

Từ thư mục `backend/`, dùng Python 3.11 để cài các thư viện của dự án.

```powershell
python --version
python -m pip install -r requirements.txt
```

Tạo `.env` từ `.env.example` nếu chưa có. Điền `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` theo PostgreSQL trên máy. `DB_COMMAND_TIMEOUT_SECONDS` giới hạn thời gian mỗi câu SQL của API, mặc định 30 giây. Với cấu hình cũ, `DATABASE_URL` được ưu tiên nếu có. Hoàn thành các bước tạo DB và seed trong database README trước khi gọi API.

## 2. Chạy API và kiểm tra

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Từ một terminal khác:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/health'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/study-areas?area_type=province'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/rainfall?data_type=observation'
Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/alerts/-1'
```

Health trả `{"status":"ok","database":"connected"}` khi truy vấn DB thành công. Swagger UI tại [localhost/docs](http://127.0.0.1:8000/docs), ReDoc tại [localhost/redoc](http://127.0.0.1:8000/redoc), hợp đồng máy đọc được tại [localhost/openapi.json](http://127.0.0.1:8000/openapi.json).

Nếu health trả `503 DATABASE_UNAVAILABLE`, dùng `psql` thử cùng host, cổng, user và tên DB trong `.env`. Ví dụ với cấu hình local trong file mẫu:

```powershell
psql -h localhost -p 5432 -U postgres -d landslide_webgis -c 'SELECT current_database(), current_user'
```

Lỗi `password authentication failed` cần kiểm tra cặp `DB_USER` và `DB_PASSWORD`. Lỗi `database "landslide_webgis" does not exist` cần tạo DB theo [hướng dẫn database](../database/README.md). Sau khi health trả 200, gọi `/api/v1/study-areas?area_type=province` để kiểm tra cả bảng và dữ liệu mẫu; kết quả mong đợi là bốn tỉnh.

## 3. Kiểm thử

Dựng và seed DB `landslide_webgis_test` theo phần 3 của database README. Từ `backend/` chạy:

```powershell
python -m pytest -q
python -m alembic check
```

Fixtures mở transaction và rollback trên DB kiểm thử, sử dụng bản ghi mẫu cố định. Pytest kiểm tra DB thật, 11 path trong OpenAPI, phân trang, lọc thời gian, lỗi 404/422/503 và chi tiết cảnh báo có các bản ghi mưa liên quan. `python -m alembic check` dùng DB phát triển đã chạy migration, kết quả mong đợi là `No new upgrade operations detected.`

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
