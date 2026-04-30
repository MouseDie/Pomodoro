.DEFAULT_GOAL := help

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env

run-gunicorn:
	gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --env-file .local.env

install:
	@echo "Installing dependency $(LIB)"
	poetry add $(LIB)

uninstall:
	@echo "Uninstalling dependency $(LIB)"
	poetry remove $(LIB)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head