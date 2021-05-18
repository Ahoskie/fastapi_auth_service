up:
	docker-compose up --build

build:
	docker-compose build

down:
	docker-compose down --remove-orphans

run:
	docker-compose exec app python $(c)

test:
	echo "No tests yet"