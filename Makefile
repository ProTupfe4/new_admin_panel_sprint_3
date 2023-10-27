up:
	docker-compose up -d

down:
	docker-compose down


admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123Qwerty@ \
	DJANGO_SUPERUSER_EMAIL=samir@mail.ru \
	docker-compose exec django-api python manage.py createsuperuser --noinput || true
