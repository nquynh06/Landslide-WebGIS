# PostgreSQL/PostGIS cho Landslide-WebGIS

[`schema.sql`](schema.sql) tạo 8 bảng nghiệp vụ, 2 bảng nối và các index. [`seed.sql`](seed.sql) nạp dữ liệu mẫu cho môi trường phát triển. Bạn có thể dựng DB bằng pgAdmin theo các bước dưới đây hoặc dùng PowerShell từ gốc repo theo mục 1–3.

## Dựng database bằng pgAdmin 4

1. **Kết nối PostgreSQL.** Trong **Servers**, mở máy chủ local và đăng nhập bằng `postgres`. Nếu chưa có kết nối, chọn **Register → Server…**, đặt tên tùy ý và điền trong tab **Connection**: host `localhost`, port `5432`, maintenance database `postgres`, username `postgres` và mật khẩu trên máy.
2. **Chọn database.** Mở `landslide_webgis`. Nếu chưa có, nhấp phải **Databases → Create → Database…**, nhập `landslide_webgis`, chọn **Owner** là `postgres`, rồi **Save**.
3. **Tạo bảng.** Mở **Query Tool mới** trên `landslide_webgis` bằng `postgres`. Trên DB chưa có bảng ứng dụng, dùng **Open File** (`Ctrl+O`) mở `database/schema.sql`, rồi nhấn **F5** để chạy toàn bộ file. Script bật PostGIS và tạo 10 bảng trong schema `public`. Nếu máy chủ báo `extension "postgis" is not available`, cài gói PostGIS tương ứng với phiên bản PostgreSQL rồi chạy lại trong tab mới.
4. **Nạp dữ liệu mẫu.** Khi schema chạy thành công, mở `database/seed.sql` và nhấn **F5**. Có thể chạy lại seed trên DB phát triển đã có bảng. [Hướng dẫn Query Tool của pgAdmin](https://www.pgadmin.org/docs/pgadmin4/latest/query_tool_toolbar.html)
5. **Kiểm tra dữ liệu.** Chạy truy vấn sau trong Query Tool. Tab **Data Output** phải có bốn tỉnh Lai Châu, Điện Biên, Sơn La và Yên Bái.

   ```sql
   SELECT name FROM study_areas WHERE area_type = 'province' ORDER BY name;
   ```

Để chạy Pytest, lặp lại bước 2–5 với tên DB `landslide_webgis_test`. Sau đó cấu hình backend theo [README backend](../backend/README.md).

## 1. Tạo role và database

Đặt thông tin kết nối cho phiên PowerShell. Đổi cổng nếu PostgreSQL trên máy dùng cổng khác.

```powershell
$env:PGHOST = '127.0.0.1'
$env:PGPORT = '5432'
$env:PGCLIENTENCODING = 'UTF8'
```

Trước khi tạo database, kết nối vào DB quản trị `postgres` để kiểm tra máy chủ có gói PostGIS và DB dự án đã tồn tại hay chưa.

```powershell
psql -X -U postgres -d postgres -c "SELECT default_version FROM pg_available_extensions WHERE name = 'postgis'" -c "SELECT datname FROM pg_database WHERE datname = 'landslide_webgis'"
```

Nếu truy vấn đầu trả 0 dòng, cài gói PostGIS cho đúng phiên bản PostgreSQL đang chạy trên Windows (ví dụ PostgreSQL 18), rồi chạy lại đến khi thấy số phiên bản PostGIS. Nếu truy vấn thứ hai trả 0 dòng, tạo DB bằng lệnh `createdb` bên dưới. Với DB đã có, bỏ qua lệnh `createdb`.

Các lệnh PowerShell dưới đây dành cho cách tách role sở hữu bảng và role chỉ đọc. Khi chạy cả schema và seed bằng `postgres` như hướng dẫn pgAdmin ở trên, hai role này là tùy chọn.

```powershell
createuser -U postgres --login --pwprompt landslide_owner
createuser -U postgres --login --pwprompt landslide_user
createdb -U postgres -O landslide_owner landslide_webgis
psql -X -v ON_ERROR_STOP=1 -U postgres -d landslide_webgis -c 'CREATE EXTENSION IF NOT EXISTS postgis' -c 'GRANT USAGE, CREATE ON SCHEMA public TO landslide_owner' -c 'GRANT USAGE ON SCHEMA public TO landslide_user'
```

Trong `backend/.env`, đặt `DB_NAME=landslide_webgis`. Nếu chạy local bằng `DB_USER=postgres` như file mẫu, điền mật khẩu của `postgres`. Để API chạy với quyền chỉ đọc, dùng `DB_USER=landslide_user` và mật khẩu tương ứng. [Mẫu cấu hình](../backend/.env.example)

## 2. Tạo bảng và nạp dữ liệu mẫu

Trên database trống đã bật PostGIS, chạy:

```powershell
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/schema.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/seed.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_user -d landslide_webgis -c "SELECT name FROM study_areas WHERE area_type = 'province' ORDER BY name"
```

Truy vấn cuối trả về Lai Châu, Điện Biên, Sơn La và Yên Bái. Có thể chạy lại seed để kiểm tra các lệnh INSERT đều báo `INSERT 0 0`.

Nếu quản lý database bằng Alembic, dùng role `landslide_owner` qua `DB_USER` và `DB_PASSWORD` trong terminal chạy migration, hoặc cấu hình riêng `MIGRATION_DATABASE_URL`. Trên DB trống ở bước 1, chạy `python -m alembic upgrade head` từ `backend/` thay cho lệnh chạy `schema.sql`, sau đó chạy `seed.sql`. Với DB đã dựng bằng SQL, chỉ dùng `python -m alembic stamp 0001` sau khi đã đối chiếu schema với revision 0001. [Hướng dẫn backend](../backend/README.md)

## 3. Database kiểm thử

Tạo DB riêng rồi dùng lại hai file SQL. Các role ở bước 1 dùng chung cho cả hai DB.

```powershell
createdb -U postgres -O landslide_owner landslide_webgis_test
psql -X -v ON_ERROR_STOP=1 -U postgres -d landslide_webgis_test -c 'CREATE EXTENSION IF NOT EXISTS postgis' -c 'GRANT USAGE, CREATE ON SCHEMA public TO landslide_owner' -c 'GRANT USAGE ON SCHEMA public TO landslide_user'
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/schema.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/seed.sql
```

Pytest mặc định dùng database `<DB_NAME>_test`. Dùng role `landslide_owner` qua `DB_USER` và `DB_PASSWORD` trong terminal chạy test, hoặc cấu hình riêng `TEST_DATABASE_URL` trỏ tới `landslide_webgis_test` bằng role này. Chạy `python -m pytest -q` từ thư mục `backend/`.
