build:
	docker-compose build --pull conversation-eval

up:
	docker-compose up conversation-eval

down:
	docker-compose down

test:
	docker-compose run --rm py311-tools tox
