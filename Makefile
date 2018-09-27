all: fs-maipo fs-ootpa

fs-base:
	./build-base.sh

fs-maipo: fs-base
	./build-maipo.sh

fs-ootpa: fs-base
	./build-ootpa.sh

clean:
	rm fs-{base,maipo,ootpa} -rf

install:
