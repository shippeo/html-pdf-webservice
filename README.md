HTML to PDF Web Service
=======================

A WSGI web service for rendering HTML to PDF using [wkhtmltopdf][1].


Running the Service
-------------------

If you are not familiar with Docker then the quickest way to get started is to
run in development mode (low performance but with auto reloading of code
changes):

 1. Make sure `wkhtmltopdf` is on your path.

 2. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

 3. Run server:

    ```sh
    python app.py
    ```

The development server listens on port 5000.

For real-world use a production-grade WSGI server should be used. The Docker
image uses Gunicorn.


Using the Service
-----------------

The web service accepts an HTML document as the "file" parameter in the body
of a URL-encoded web form POST request and responds with the rendered PDF. For
example:

```sh
cat sample.html | curl -X POST -F file=@- http://localhost:5000/ > output.pdf
```


Running as Docker Container
---------------------------

To run the service as a Docker container:

 1. Build the Docker image:

    ```sh
    docker build -t html-pdf-webservice .
    ```

 2. Run a Docker container (binding to port 5000):

    ```sh
    docker run -p 5000:80 html-pdf-webservice
    ```

The entry point for the container is the Gunicorn server and the default args
use the server config in `config.py`. Server config can be modified in
`config.py` or provided as args to the container entry point. For example, to
launch the container, overriding the default worker count:

```sh
docker run -p 5000:80 html-pdf-webservice -c config.py -w 32 app:application
```

See the [Gunicorn settings][2] docs for more details.


## Performance Testing

The rendering performance is dependent on the contents of the submitted HTML
documents. In particular, documents with a lot of images will result in slower
rendering but will be more I/O bound while images are being loaded so should
be capable of more parallelism.

The performance test script is written using [locust.io][3].
It uploads HTML documents every 4-9 seconds per user. To run the test:

 1. Install test dependencies:

    ```sh
    pip install -r requirements-test.txt
    ```

 2. Run Locust server:

    ```sh
    locust --host http://localhost:5000
    ```

 3. Load the Locust web interface at http://localhost:8089 and create a user
    swarm.

The HTML documents submitted during the test should be adjusted so they are
similar in structure to those expected to be rendered in the production
setting. The number of Gunicorn worker processes should likewise be tweaked to
maximize throughput for those documents.


[1]: http://wkhtmltopdf.org/
[2]: http://docs.gunicorn.org/en/latest/settings.html
[3]: http://locust.io/
