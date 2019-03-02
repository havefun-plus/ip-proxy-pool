isort:
	isort -rc .    

lint:
	flake8 --format=pylint --count --exit-zero ipfeeder tests

clean:
	find . -iname "*__pycache__" | xargs rm -rf
	find . -iname "*.pyc" | xargs rm -rf

docker-run:
	docker build -t="havefun-plus/ip-proxy-pool:v1" .
	docker-compose up

