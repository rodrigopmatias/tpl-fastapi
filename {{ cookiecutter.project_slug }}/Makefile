# vim: noexpandtab filetype=make

PROJET_NAME=$(shell basename ${PWD})
REGISTRY_SERVICE=localhost:5000
PKG_MODULE=$(shell echo $(PROJET_NAME) | sed -s "s/-/_/gi")
APP_PORT=8000
APP_HOST=127.0.0.1
APP_VERSION=$(shell poetry version -s)
INSTALL_EXTRAS=all

IMAGE_BASE=$(REGISTRY_SERVICE)/matias/$(PROJET_NAME)
IMAGE_TARGET=$(IMAGE_BASE):v$(APP_VERSION)

run: install
	poetry run uvicorn --factory "$(PKG_MODULE):create_app" --port $(APP_PORT) --host $(APP_HOST)

install:
	poetry install -E $(INSTALL_EXTRAS)

linter:
	poetry run pre-commit run -av

test:
	poetry run pytest

container.env:
	touch container.env

container: build container.env
	podman container run --rm --env-file container.env -it -p $(APP_PORT):8000 $(IMAGE_TARGET)

push: build
	podman image push $(IMAGE_TARGET)

build:
	podman image build -t $(IMAGE_TARGET) .

image-clear:
	scripts/image-clear.sh $(IMAGE_BASE)

clear: image-clear
	rm -fr .pytest_cache
	rm -fr .skjold_cache
	rm -f  .coverage
