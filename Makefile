PACKAGE ?= batvoice-labelit
DOCKER ?= $(shell which docker || echo docker)
DOCKER_VARY ?=
DOCKER_IMAGE ?= 367353094751.dkr.ecr.eu-west-1.amazonaws.com/$(shell echo $(PACKAGE) | tr A-Z a-z)-$(DOCKER_VARY)
VERSION ?= $(shell git describe --abbrev=8 --always HEAD)
DOCKER_TAG ?= $(VERSION)
DOCKER_BUILD ?= $(DOCKER) image build
DOCKER_PUSH ?= $(DOCKER) image push
DOCKER_BUILD_FILE ?= dockerfile.$(DOCKER_VARY).prod

DOCKER_BUILD_OPTIONS ?= --build-arg IMAGE=$(DOCKER_IMAGE) --build-arg TAG=$(DOCKER_TAG)

docker-aws-ecr-login:   ## Apply AWS credentials for the container registry to local docker.
	$(shell aws ecr get-login --no-include-email --region eu-west-1)
docker-build-backend: 
	DOCKER_VARY=backend $(MAKE) docker-build 
docker-push-backend: 
	DOCKER_VARY=backend $(MAKE) docker-push
docker-build-frontend:   ## Build a docker image.
	DOCKER_VARY=frontend $(MAKE) docker-build 
docker-push-frontend: 
	DOCKER_VARY=frontend $(MAKE) docker-push
docker-build:   ## Build a docker image.
	$(DOCKER_BUILD) -f $(DOCKER_BUILD_FILE) $(DOCKER_BUILD_OPTIONS) -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
docker-push: docker-aws-ecr-login ## Push docker image to remote registry.
	$(DOCKER_PUSH) $(DOCKER_PUSH_OPTIONS) $(DOCKER_IMAGE):$(DOCKER_TAG)

help:   ## Shows available commands.
	@echo "Available commands:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?##[\s]?.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "	make \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo
