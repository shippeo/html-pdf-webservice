import re
from locust import HttpLocust, TaskSet


wikipedia_main_page_html = "wikipedia-main-page.html"


def print_document(l, html_file_name):
    with open(html_file_name, "r") as html_file:
        l.client.post(
            url="/",
            files={
                "file": html_file
            }
        )


def print_simple_document(l):
    print_document(l, "sample.html")


def print_wikipedia_home_page(l):
    print_document(l, wikipedia_main_page_html)


def download_wikipedia_home_page(l):
    response = l.client.get("https://en.wikipedia.org/wiki/Main_Page")
    # External CSS and image links will be in scheme-relative form, such as
    # "//host/path". These URLs will break when the page is loaded with the
    # file:// scheme by wkhtmltopdf. Replace them with https:// URLs.
    html = re.sub('([^:])//', r'\1https://', response.text)
    with open(wikipedia_main_page_html, "w") as f:
        f.write(html.encode('utf8'))


class UserBehavior(TaskSet):
    tasks = {
        print_simple_document: 1,
        print_wikipedia_home_page: 1,
    }

    def on_start(self):
        download_wikipedia_home_page(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
