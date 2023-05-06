run:
	python3.11 src/main.py encrypt theblockbreakers 2b7e151628aed2a6abf7158809cf4f3c
	python3.11 src/main.py decrypt c69f25d0025a9ef32393f63e2f05b747 2b7e151628aed2a6abf7158809cf4f3c
	python3.11 src/main.py attack

test:
	python3.11 src/unittests.py -v

clean:
	-rm -rf src/__pycache__