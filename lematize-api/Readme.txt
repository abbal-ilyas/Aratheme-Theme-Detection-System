The Rest API can be used from several languages such as Java and Python. 
To run the Rest API on your local machine:  
  1) You need java version 17 or higher 
  2) Run: 
        java -jar Rest-API-LemmaRootStem.jar

This will start a local server running on port 8080 on your machine. 

"test_lemma.py", "test_root.py" and "test_stem.py" are examples of Python code calling the Rest API from your local machine.


You can use Docker to run the Rest API from any unused port of your machine. A Docker file is provided. 

    1) Install Docker if not already installed (https://docs.docker.com/engine/install)
    2) Build the parser image:
        docker build -t lemma-root-stem .
    3) Run Docker on any port, for example 8084:
        docker run -p 8084:8080 lemma-root-stem
    3) Change the URL in "test_lemma.py" as follows:
        url = 'http://localhost:8084/api/lemma'

Enjoy!
