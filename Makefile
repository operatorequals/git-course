REPO=operatorequals/
IMAGE=git-course
VERSION=0.1.0
# 'ssh' and 'http'
TYPE=http

challenges:
	for repo in challenge*; do cp generic/* repos/$${repo}.git/hooks/; cp $${repo}/* repos/$${repo}.git/hooks/; done

image: challenges
	docker build -t $(REPO)$(IMAGE)-$(TYPE):$(VERSION) . -f deploy/$(TYPE).Dockerfile
	docker tag $(REPO)$(IMAGE)-$(TYPE):$(VERSION) $(REPO)$(IMAGE)-$(TYPE):latest

push: image
	docker push $(REPO)$(IMAGE)-$(TYPE):$(VERSION)

heroku-push: challenges
	cd deploy/ && \
	cp $(TYPE).Dockerfile Dockerfile && \
	heroku container:push web -a git-interactive-course -v --context-path ../ && \
	rm Dockerfile && \
	cd ../ 

heroku-release: heroku-push
	heroku container:release -a git-interactive-course web

clean:
	for repo in repos/challenge*.git; do rm -rf $$repo/hooks/*; done
	docker image rm $(REPO)$(IMAGE)-$(TYPE):$(VERSION)

