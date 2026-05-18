# DB 테이블 정보 추출 SQL

Olfit backend는 Django 설정 기준으로 MySQL을 사용한다. 테이블, 컬럼, 인덱스, 외래키 정보는 MySQL의 `information_schema`에서 조회할 수 있다.

## DB 접속

Docker Compose 환경에서는 다음 명령으로 MySQL에 접속한다.

```bash
docker compose exec database mysql -u olfit_admin -p olfit_db
```

비밀번호는 `.env` 또는 `.env.example`의 `SQL_DB_PASSWORD` 값을 사용한다.

## 테이블 목록

```sql
SELECT
  table_name,
  table_type,
  table_rows,
  create_time,
  update_time
FROM information_schema.tables
WHERE table_schema = 'olfit_db'
ORDER BY table_name;
```

## 컬럼 상세

```sql
SELECT
  table_name,
  ordinal_position,
  column_name,
  column_type,
  is_nullable,
  column_default,
  column_key,
  extra,
  column_comment
FROM information_schema.columns
WHERE table_schema = 'olfit_db'
ORDER BY table_name, ordinal_position;
```

## 인덱스 정보

```sql
SELECT
  table_name,
  index_name,
  non_unique,
  seq_in_index,
  column_name
FROM information_schema.statistics
WHERE table_schema = 'olfit_db'
ORDER BY table_name, index_name, seq_in_index;
```

## 외래키 정보

```sql
SELECT
  table_name,
  column_name,
  referenced_table_name,
  referenced_column_name,
  constraint_name
FROM information_schema.key_column_usage
WHERE table_schema = 'olfit_db'
  AND referenced_table_name IS NOT NULL
ORDER BY table_name, column_name;
```

## 테이블별 row 수 요약

```sql
SELECT
  table_name,
  table_rows
FROM information_schema.tables
WHERE table_schema = 'olfit_db'
  AND table_type = 'BASE TABLE'
ORDER BY table_rows DESC, table_name;
```

`information_schema.tables.table_rows` 값은 MySQL 스토리지 엔진에 따라 추정치일 수 있다. 정확한 row 수가 필요하면 각 테이블에 대해 `COUNT(*)`를 별도로 실행한다.
