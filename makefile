up:
	docker-compose up -d

down:
	docker-compose down -v

init_db:
	python -m backend.database.init_db

extract:
	python -m backend.scripts.extract_usgs_historical_earthquake_data
	python -m backend.scripts.extract_gem_fault_data

transform:
	python -m backend.scripts.transform_earthquake_data

load:
	python -m backend.scripts.load_data_postgis

etl:
	make extract
	make transform
	make load

setup:
	make init_db
	make etl

fastapi:
	uvicorn backend.app.main:app --reload