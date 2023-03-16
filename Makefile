run_tests:
	docker compose -f docker-compose.test.yml up --build test-web
	docker compose -f docker-compose.test.yml down -v --remove-orphans

compose_up:
	docker compose -f docker-compose.yml up

compose_up_with_build:
	docker compose -f docker-compose.yml up --build

