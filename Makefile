.PHONY: help setup start stop restart logs clean seed test health

help: ## Show this help message
	@echo "Language Tutor With Langflow - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup: copy .env.example to .env
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file. Please edit it and add your OPENAI_API_KEY"; \
	else \
		echo "⚠️  .env file already exists. Skipping..."; \
	fi

start: ## Start all services (Langflow + PostgreSQL)
	docker compose up -d
	@echo "⏳ Waiting for services to start..."
	@sleep 5
	@echo "✅ Services started!"
	@echo "   - Langflow: http://localhost:7860"
	@echo "   - PostgreSQL: localhost:5432"

stop: ## Stop all services
	docker compose down
	@echo "✅ Services stopped"

restart: stop start ## Restart all services

logs: ## Show logs from all services
	docker compose logs -f

logs-langflow: ## Show logs from Langflow only
	docker compose logs -f langflow

logs-postgres: ## Show logs from PostgreSQL only
	docker compose logs -f postgres

clean: ## Stop services and remove volumes (WARNING: deletes database data)
	docker compose down -v
	@echo "✅ Services stopped and volumes removed"

seed: ## Seed the database with sample vocabulary
	@echo "📚 Seeding vocabulary database..."
	@pip install -q psycopg2-binary
	@python scripts/seed_db.py
	@echo "✅ Database seeded successfully"

health: ## Check health status of all services
	@echo "Checking service health..."
	@python scripts/health_check.py

test: ## Run tests for custom components
	@echo "🧪 Running tests..."
	@pip install -q pytest psycopg2-binary
	@pytest tests/ -v

install-deps: ## Install Python dependencies for local development
	pip install -r scripts/requirements.txt
	pip install pytest pytest-mock

status: ## Show status of all containers
	@docker compose ps

shell-langflow: ## Open a shell in the Langflow container
	docker compose exec langflow /bin/bash

shell-postgres: ## Open a PostgreSQL shell
	docker compose exec postgres psql -U langflow -d langflow_db

backup-db: ## Backup the vocabulary database
	@mkdir -p backups
	@docker compose exec -T postgres pg_dump -U langflow langflow_db > backups/vocab_backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backed up to backups/"

restore-db: ## Restore database from backup (usage: make restore-db FILE=backups/vocab_backup_XXXXXXXX.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify FILE=path/to/backup.sql"; \
		exit 1; \
	fi
	@docker compose exec -T postgres psql -U langflow langflow_db < $(FILE)
	@echo "✅ Database restored from $(FILE)"

dev-setup: setup install-deps start seed ## Complete development setup
	@echo ""
	@echo "🎉 Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env and add your OPENAI_API_KEY"
	@echo "2. Visit http://localhost:7860"
	@echo "3. Import flows/language_tutor_flow.json"
	@echo "4. Configure OpenAI API key in the flow"
	@echo "5. Start chatting with your language tutor!"

