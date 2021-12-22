STACK_NAME:=da-black-belt-2021

check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

build: clean mkdirs download scripts

clean:
	rm -rf build
	
mkdirs:
	mkdir -p build/emr/jars

download:
	curl https://jdbc.postgresql.org/download/postgresql-42.3.1.jar -o build/emr/jars/postgresql-42.3.1.jar

scripts:
	cp -r src/emr/ build/emr/

deploy: $(call check_defined, STACK_NAME)
deploy:
	BUCKET=`aws ssm get-parameter --name /$(STACK_NAME)/cicd/artifact_bucket/name | jq -r .Parameter.Value ` ;\
	aws s3 sync build s3://$$BUCKET/artifacts/
