
.PHONY: build
build:
	sudo docker-compose build

.PHONY: start
start:
	docker-compose up --no-attach mongo

.PHONY: stop
stop:
	docker-compose stop

.PHONY: clean
clean:
	sudo rm -rf .artifacts
	sudo docker system prune

.PHONY: restart
restart:
	make clean
	make build
	make start