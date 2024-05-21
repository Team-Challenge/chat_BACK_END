
IMAGE_NAME = rudychuk/fastapi-chat
IMAGE_NAME_ARM = rudychuk/fastapi-chat-arm
TAG = latest

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

build_arm:
	docker build -t $(IMAGE_NAME_ARM):$(TAG) .

login:
	echo $(DOCKER_PASSWORD) | docker login -u $(DOCKER_USERNAME) --password-stdin

push: login
	docker push $(IMAGE_NAME):$(TAG)

push_arm: login
	docker push $(IMAGE_NAME_ARM):$(TAG)


#example DOCKER_USERNAME=your_dockerhub_username DOCKER_PASSWORD=your_dockerhub_password make all
all: build push

all_arm: build_arm push_arm

