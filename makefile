VERSION := local

build b:
	docker build . -t docker.io/brianwolf94/docker-sync:$(VERSION)


push p:
	docker push docker.io/brianwolf94/docker-sync:$(VERSION)


run r:
	docker run -it --rm --name docker-sync -p 5000:5000 docker.io/brianwolf94/docker-sync:$(VERSION)