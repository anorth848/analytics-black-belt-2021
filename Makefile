

build: clean mkdirs download scripts

clean:
	rm -rf build
	
mkdirs:
	mkdir -p build/emr/jars

download:
	curl https://jdbc.postgresql.org/download/postgresql-42.3.1.jar -o build/emr/jars/postgresql-42.3.1.jar

scripts:
	cp -r src/emr/ build/emr/

deploy: upload

upload:
	aws s3 sync build s3://$(BUCKET)/analytics-black-belt-2021/
