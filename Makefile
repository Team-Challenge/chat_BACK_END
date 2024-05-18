
IMAGE_NAME = rudychuk/fastapi-chat
TAG = latest

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

login:
	echo $(DOCKER_PASSWORD) | docker login -u $(DOCKER_USERNAME) --password-stdin

push: login
	docker push $(IMAGE_NAME):$(TAG)


#example DOCKER_USERNAME=your_dockerhub_username DOCKER_PASSWORD=your_dockerhub_password make all
all: build push

