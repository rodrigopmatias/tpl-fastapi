# vim: noexpandtab filetype=make

PROJET_NAME=$(shell basename ${PWD})
REGISTRY_SERVICE=localhost:5000
PKG_MODULE=$(shell echo $(PROJET_NAME) | sed -s "s/-/_/gi")
APP_PORT=8000
APP_HOST=127.0.0.1
POETRY_EXTRA_ARGS=

CURRENT_BRANCH=$(shell git branch --show-current)
ifeq ($(CURRENT_BRANCH), main)
	APP_VERSION=$(shell poetry version -s)
else ifeq ($(CURRENT_BRANCH), stage)
	APP_VERSION=$(shell poetry version -s)-rev.$(shell git rev-parse --short HEAD)
else
	APP_VERSION=$(shell poetry version -s)-dev.$(shell git rev-parse --short HEAD)
endif
IMAGE_BASE=$(REGISTRY_SERVICE)/matias/$(PROJET_NAME)
IMAGE_TARGET=$(IMAGE_BASE):v$(APP_VERSION)
CONTAINER_PLATFORM="linux/amd64"
GITHUB_AUTHORIZATION=

dev.env:
	@echo BROKER_DRY=y > dev.env

run/dev: install dev.env
	poetry run uvicorn --factory "$(PKG_MODULE):create_app" --port $(APP_PORT) --host $(APP_HOST) --reload

run: install
	poetry run uvicorn --factory "$(PKG_MODULE):create_app" --port $(APP_PORT) --host $(APP_HOST)

install:
	poetry install ${POETRY_EXTRA_ARGS}

linter:
	poetry run pre-commit run -av

test:
	poetry run pytest

container.env:
	touch container.env

container: build container.env
	podman container run \
		--platform "$(CONTAINER_PLATFORM)" \
		--rm \
		--env-file container.env \
		-it \
		-p $(APP_PORT):8000 $(IMAGE_TARGET)

push: build
	podman image push $(IMAGE_TARGET)

build:
	podman image build \
		--build-arg GITHUB_AUTHORIZATION="$(GITHUB_AUTHORIZATION)" \
		--build-arg POETRY_EXTRA_ARGS="$(POETRY_EXTRA_ARGS)" \
		-t $(IMAGE_TARGET) .

image-clear:
	scripts/image-clear.sh $(IMAGE_BASE)

clear: image-clear
	rm -fr .pytest_cache
	rm -fr .skjold_cache
	rm -f  .coverage
