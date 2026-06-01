.PHONY: all
all: Containerfile-10.1
all: Containerfile-10.2

.PHONY: clean
clean:
	rm -f Containerfile-10.*

Containerfile-10.%: Containerfile-vault
	env release=10.$* envsubst '$$release' <Containerfile-vault >$@

Containerfile-10.2: Containerfile-fixed
	env release=10.2 envsubst '$$release' <Containerfile-fixed >$@
