.PHONY: migrate
migrate:
	alembic migrate head

.PHONY: dock
dock:
	docker build . --file=infra/server.dockerfile --tag="vladmarlo/enrollment_backend:latest"
	docker build . --file=infra/migrator.dockerfile --tag="vladmarlo/enrollment_migrator:latest"

.PHONY: dock/push
dock/push: dock
	docker push vladmarlo/enrollment_backend:latest
	docker push vladmarlo/enrollment_migrator:latest

.PHONY: dock/run
dock/run:
	docker-compose up -d

.PHONY: lines
lines:
	git ls-files | xargs wc -l
