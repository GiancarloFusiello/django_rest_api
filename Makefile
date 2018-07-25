
help:
	@echo "start           - run the server"
	@echo "stop            - stops any running servers including background services"
	@echo "migrate         - run django database migrations"
	@echo "createsuperuser - a shortcut for add an admin to the database"
	@echo "test            - run tests"

start:
	docker-compose up

stop:
	docker-compose down

migrate:
	docker-compose run --rm web python manage.py migrate

createsuperuser:
	docker-compose run --rm web python manage.py createsuperuser

test:
	docker-compose run --rm web python manage.py test
