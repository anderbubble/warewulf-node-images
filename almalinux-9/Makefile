.PHONY: all
all: Containerfile-9.7
all: Containerfile-9.8

.PHONY: clean
clean:
	rm -f Containerfile-9.*

Containerfile-9.%: Containerfile-vault
	env release=9.$* envsubst '$$release' <Containerfile-vault >$@

Containerfile-9.8: Containerfile-fixed
	env release=9.8 envsubst '$$release' <Containerfile-fixed >$@
