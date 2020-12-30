build:
	docker build --tag=bandbase .

run:
	docker run -it -p=5432:5432 -v ~:/data --name=bandbase bandbase

rm:
	docker rm bandbase
