Create `docker-compose.yml`:
```
nano docker-compose.yml
or
touch docker-compose.yml
```
```
version: "3.9"

services:
  db:
    image: supabase/postgres:15.1.0.117
    container_name: supabase-db
    restart: always
    ports:
      - "54322:5432"
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - db-data:/var/lib/postgresql/data

  rest:
    image: postgrest/postgrest:v11.2.0
    container_name: supabase-rest
    depends_on:
      - db
    environment:
      PGRST_DB_URI: postgres://postgres:postgres@db:5432/postgres
      PGRST_DB_SCHEMA: public
      PGRST_DB_ANON_ROLE: anon
    ports:
      - "54321:3000"

  studio:
    image: supabase/studio:latest
    container_name: supabase-studio
    depends_on:
      - db
    ports:
      - "54323:3000"

volumes:
  db-data:
```
Start Supabase Services
```
docker compose up -d
```
Check Running Containers:
```
docker ps
```
Access Supabase

> REST API:	http://localhost:54321

> Postgres: localhost:54322

> Studio: http://localhost:54323

Connect from Python
```
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=54322,
    database="postgres",
    user="postgres",
    password="postgres"
)
```
Enable pgvector
```
docker exec -it supabase-db psql -U postgres
```
Inside psql:
```
CREATE EXTENSION IF NOT EXISTS vector;
```
Stop Supabase and Keep Data:
```
docker compose down
```
Delete Everything:
```
docker compose down -v
```