#! /usr/bin/env python
"""
    WSGI APP to convert wkhtmltopdf As a webservice

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import shutil
from subprocess import Popen, PIPE

from werkzeug.wsgi import wrap_file
from werkzeug.exceptions import MethodNotAllowed, BadRequest
from werkzeug.wrappers import Request, Response


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
    process = Popen(['wkhtmltopdf', '-', '-'], stdin=PIPE, stdout=PIPE)
    shutil.copyfileobj(request.files['file'], process.stdin)
    process.stdin.close()
    return Response(
        wrap_file(request.environ, process.stdout),
        mimetype='application/pdf',
    )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
