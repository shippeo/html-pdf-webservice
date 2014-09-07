#! /usr/bin/env python
"""
    WSGI APP to convert wkhtmltopdf As a webservice

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import tempfile

from werkzeug.wsgi import wrap_file
from werkzeug.exceptions import MethodNotAllowed, BadRequest
from werkzeug.wrappers import Request, Response
from executor import execute


@Request.application
def application(request):
    """
    Accepts a POST request with a form encoded body with a single "file" form
    field which is expected to have an HTML document as the value. The
    response body will contain a PDF rendering of the input HTML file.
    """
    if request.method != 'POST':
        return MethodNotAllowed('POST')
    if not request.files.get('file'):
        return BadRequest('file is required')

    with tempfile.NamedTemporaryFile(suffix='.html') as source_file:

        if request.files:
            # First check if any files were uploaded
            source_file.write(request.files['file'].read())

        source_file.flush()

        # Evaluate argument to run with subprocess
        args = ['wkhtmltopdf']

        # Add source file name and output file name
        file_name = source_file.name
        args += [file_name, file_name + ".pdf"]

        # Execute the command using executor
        execute(' '.join(args))

        return Response(
            wrap_file(request.environ, open(file_name + '.pdf')),
            mimetype='application/pdf',
        )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
