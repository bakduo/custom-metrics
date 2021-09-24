DIST=./dist

build:
		mkdir $(DIST)
		cp -r app $(DIST)
		cp Dockerfile $(DIST)
		cp run.py main.py Pip* $(DIST)
		ls -la $(DIST)
		cd $(DIST) && docker build --rm -t monitor-app:1.0.0 .

clean:
		rm -rf $(DIST)
