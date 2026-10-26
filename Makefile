PKG := $(CURDIR)

.PHONY: install build test clean

install:
	npm install

build:
	npm run build

test:
	npm test

clean:
	rm -rf dist typescript/dist typescript/test-dist node_modules
	rm -f typescript/src/lib/remotion-primitives.generated.js
