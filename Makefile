all: fs-ootpa

fs-base:
	./build-base.sh

fs-ootpa: fs-base
	./build-ootpa.sh

clean:
	rm fs-{base,ootpa} -rf

install:
