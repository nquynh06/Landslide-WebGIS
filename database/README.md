# PostgreSQL/PostGIS cho Landslide-WebGIS

M1 cung cấp 8 bảng nghiệp vụ và 2 bảng nối. Bản đã kiểm tra dùng PostgreSQL 17.5, PostGIS 3.5.2 và Python 3.11.17. Container chỉ nhận kết nối qua localhost, mặc định cổng 55432. Volume `landslide-webgis_landslide_data` giữ dữ liệu qua các lần dừng/khởi động.

## 1. Khởi tạo trên Windows với Docker Desktop

Chạy PowerShell từ **gốc repo**. Cần Docker Compose, Python 3.11 và PostgreSQL client (`psql`, `createdb`) trên PATH. Các lệnh sau dùng biến môi trường của process hiện tại.

```powershell
Copy-Item -LiteralPath backend/.env.example -Destination backend/.env
```

Thực hiện lệnh sao chép **một lần** cho máy mới. Trong `backend/.env`, thay ba mật khẩu mẫu bằng ba giá trị riêng, cập nhật mật khẩu và cổng tương ứng trong cả ba URL. Chuỗi hex ngẫu nhiên dùng được trực tiếp trong URL. Nếu mật khẩu có ký tự đặc biệt, percent-encode phần mật khẩu trong URL. Lưu file UTF-8. Để mở lại dự án đã thiết lập, dùng file hiện có.

```powershell
docker compose --env-file backend/.env -f database/compose.yaml up -d --wait
```

Ở lần tạo volume, image khởi tạo database `landslide_webgis`. Entrypoint chạy `database/bootstrap.sql` để bật PostGIS và tạo hai role. `landslide_owner` tạo schema và chạy migration; `landslide_user` đọc các bảng nghiệp vụ qua API. Password trong file env cần khớp với role đã tạo khi dùng lại volume.

**Nếu dùng PostgreSQL cài trực tiếp**, cài extension PostGIS tương ứng phiên bản PostgreSQL, tạo DB bằng `createdb -U postgres landslide_webgis`. Đặt biến môi trường `LANDSLIDE_OWNER_PASSWORD` và `LANDSLIDE_APP_PASSWORD`, chạy `psql -X -U postgres -d landslide_webgis -f database/bootstrap.sql` rồi cấu hình URL trỏ đúng máy/cổng. Hai đường cài dùng cùng schema.

## 2. Dựng schema và seed phát triển

Cài venv theo phần 1 của [backend README](../backend/README.md). **Trên một DB trống, chọn một trong hai đường dựng schema.** Cách chuẩn cho môi trường phát triển là Alembic:

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic check
Pop-Location
```

Để dùng psql, nạp thông số cho terminal hiện tại. Đoạn này đọc các khóa mật khẩu/cổng trong file env đơn giản của ví dụ, không in giá trị.

```powershell
Get-Content -LiteralPath backend/.env | ForEach-Object {
    if ($_ -match '^(POSTGRES_PASSWORD|LANDSLIDE_OWNER_PASSWORD|LANDSLIDE_APP_PASSWORD|POSTGRES_PORT)=(.+)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
$env:PGHOST = '127.0.0.1'
$env:PGPORT = if ($env:POSTGRES_PORT) { $env:POSTGRES_PORT } else { '55432' }
$env:PGCLIENTENCODING = 'UTF8'
$env:PGPASSWORD = $env:LANDSLIDE_OWNER_PASSWORD
```

Đường dựng SQL độc lập, dùng trên **DB còn trống đã bootstrap**:

```powershell
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/schema.sql
```

Sau một trong hai đường dựng, nạp dữ liệu mẫu vào DB phát triển rồi kiểm tra quyền đọc và liên kết:

```powershell
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis -f database/seed.sql
$env:PGPASSWORD = $env:LANDSLIDE_APP_PASSWORD
psql -X -U landslide_user -d landslide_webgis -f database/verify.sql
```

Seed chạy trong một transaction và có thể chạy lại. Bốn tỉnh và vùng tổng hợp có ID tự sinh; ID âm dành riêng cho dữ liệu mẫu. Rubric, hình học thật và legend chờ GIS bàn giao. `verify.sql` trả phiên bản PostGIS và hoàn thành khối `DO` khi seed và SRID đúng.

## 3. DB kiểm thử riêng và đối chiếu

Dùng cùng phiên PowerShell đã nạp biến ở trên, tạo DB kiểm thử mới **một lần**. DB này được dựng bằng SQL để kiểm tra song song với DB phát triển dựng bằng Alembic.

```powershell
$env:PGPASSWORD = $env:POSTGRES_PASSWORD
createdb -U postgres landslide_webgis_test
psql -X -U postgres -d landslide_webgis_test -f database/bootstrap.sql
$env:PGPASSWORD = $env:LANDSLIDE_OWNER_PASSWORD
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/schema.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/seed.sql
psql -X -v ON_ERROR_STOP=1 -U landslide_owner -d landslide_webgis_test -f database/seed.sql
psql -X -U landslide_owner -d landslide_webgis_test -f database/verify.sql
```

Lần seed thứ hai phải báo `INSERT 0 0` cho các lệnh INSERT. Chạy Pytest theo backend README để kiểm tra khóa chính, FK, trùng liên kết, SRID và quyền đọc. Để so hai cách cài ở mức DDL, chạy đoạn sau trên hai DB đã dựng cùng phiên bản. Kiểm tra cả sequences, khóa, index và GRANT; loại bảng ghi phiên bản Alembic và đối tượng do extension tạo.

```powershell
$tables = 'study_areas','data_sources','gis_layers','rubric_criteria','susceptibility_maps','landslide_events','rainfall_records','alerts'
$links = 'gis_layer_study_areas','alert_rainfall_records'
$objects = @(($tables + $links) | ForEach-Object { "--table=public.$_" })
$objects += @($tables | ForEach-Object { "--table=public.${_}_id_seq" })
function Read-AppSchema($databaseName) {
    $ddl = pg_dump -U landslide_owner --schema-only --no-owner @objects $databaseName
    if ($LASTEXITCODE) { throw "pg_dump failed for $databaseName" }
    $ddl -notmatch '^\\(un)?restrict'
}
Compare-Object (Read-AppSchema landslide_webgis) (Read-AppSchema landslide_webgis_test) -SyncWindow 0
```

Kết quả so sánh rỗng nghĩa là DDL ứng dụng trùng nhau. Nếu chuyển DB tạo bằng SQL sang Alembic, trước hết đối chiếu với một DB tham chiếu dựng bằng đúng revision; chỉ khi trùng mới chạy `alembic stamp 0001` ở baseline này. Tất cả revision nằm trong `backend/migrations/versions/`. Khi đổi schema, thêm revision mới, cập nhật `database/schema.sql`, ORM và [thiết kế DB](../docs/database_design.md). Giữ nguyên SQL đóng băng của revision cũ.

Dừng DB và giữ volume bằng `docker compose --env-file backend/.env -f database/compose.yaml stop`. Lần sau chạy lại lệnh `up -d --wait`.
