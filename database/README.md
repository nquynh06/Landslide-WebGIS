# PostgreSQL/PostGIS cho Landslide-WebGIS

[`schema.sql`](schema.sql) tạo 8 bảng nghiệp vụ, 2 bảng nối và các index. [`seed.sql`](seed.sql) nạp dữ liệu mẫu cho môi trường phát triển. Chạy các lệnh PowerShell bên dưới từ gốc repo với PostgreSQL, PostGIS và bộ công cụ dòng lệnh PostgreSQL đã cài trên máy.

## 1. Tạo role và database

Đặt thông tin kết nối cho phiên PowerShell. Đổi cổng nếu PostgreSQL trên máy dùng cổng khác.

```powershell
$env:PGHOST = '127.0.0.1'
$env:PGPORT = '5432'
$env:PGCLIENTENCODING = 'UTF8'
```

Trên PostgreSQL mới, tạo hai role một lần. `--pwprompt` yêu cầu nhập mật khẩu cho role mới. Nếu các role đã có, dùng lại và chuyển sang bước tạo database.

```powershell
createuser -U postgres --login --pwprompt landslide_owner
createuser -U postgres --login --pwprompt landslide_user
createdb -U postgres -O landslide_owner landslide_webgis
psql -X -v ON_ERROR_STOP=1 -U postgres -d landslide_webgis -c 'CREATE EXTENSION IF NOT EXISTS postgis' -c 'GRANT USAGE, CREATE ON SCHEMA public TO landslide_owner' -c 'GRANT USAGE ON SCHEMA public TO landslide_user'
```

Trong `backend/.env`, đặt `DATABASE_URL` cho role đọc `landslide_user`, `MIGRATION_DATABASE_URL` cho `landslide_owner`, cùng host, cổng và mật khẩu đã chọn. [Mẫu cấu hình](../backend/.env.example)

## 2. Tạo bảng và nạp dữ liệu mẫu

Trên database trống đã bật PostGIS, chạy:

```powershell
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/schema.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/seed.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_user -d landslide_webgis -c "SELECT name FROM study_areas WHERE area_type = 'province' ORDER BY name"
```

Truy vấn cuối trả về Lai Châu, Điện Biên, Sơn La và Yên Bái. Có thể chạy lại seed để kiểm tra các lệnh INSERT đều báo `INSERT 0 0`.

Nếu quản lý database bằng Alembic, trên DB trống ở bước 1 dùng `alembic upgrade head` từ `backend/` thay cho lệnh chạy `schema.sql`, sau đó chạy `seed.sql` như trên. Với DB đã dựng bằng SQL, chỉ dùng `alembic stamp 0001` sau khi đã đối chiếu schema với revision 0001. [Hướng dẫn backend](../backend/README.md)

## 3. Database kiểm thử

Tạo DB riêng rồi dùng lại hai file SQL. Các role ở bước 1 dùng chung cho cả hai DB.

```powershell
createdb -U postgres -O landslide_owner landslide_webgis_test
psql -X -v ON_ERROR_STOP=1 -U postgres -d landslide_webgis_test -c 'CREATE EXTENSION IF NOT EXISTS postgis' -c 'GRANT USAGE, CREATE ON SCHEMA public TO landslide_owner' -c 'GRANT USAGE ON SCHEMA public TO landslide_user'
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/schema.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/seed.sql
```

Đặt `TEST_DATABASE_URL` trỏ tới `landslide_webgis_test` bằng role `landslide_owner`. Chạy `python -m pytest -q` trong venv từ thư mục `backend/` để kiểm tra khóa, SRID, quyền và các API.
