EN:

Start using docker command:

docker-compose -f "docker-compose.yml" up -d --build

then you can run pgadmin (http://localhost:3838) and log in using:

username: admin
password: edsr0241ygserd4520457yudr356fd4gh54fgd7h654165gh43dfxt6jh43fd

and flower (http://localhost:1300) to watch database changes and tasks live

PL:

Zacznij używając komendy dockera:

docker-compose -f "docker-compose.yml" up -d --build

wtedy możesz uruchomić panel PGAdmin (http://localhost:3838)  i zalogować się używając:

użytkownik: admin
hasło: edsr0241ygserd4520457yudr356fd4gh54fgd7h654165gh43dfxt6jh43fd

a także flower (http://localhost:1300), aby obserwować zmiany w bazie danych i w taskach Celery na żywo.