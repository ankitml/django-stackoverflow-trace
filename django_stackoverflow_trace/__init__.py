from django.views import debug
from django.conf import settings


def get_search_links():
    default_choice = "stackoverflow"

    search_urls = {
        "stackoverflow": "http://stackoverflow.com/search?q=[python] or "
                         "[django]+{{ exception_value|force_escape }}",
        "googlesearch": "https://www.google.com.tr/#q="
                        "+django+{{ exception_value|force_escape }}"
    }

    return list(search_urls.values())


def _patch_django_debug_view():

    new_data = """
        <h3 style="margin-bottom:10px;">
            <a href="{0}"
             target="_blank">View in Stackoverflow</a>
        </h3>
        <h3 style="margin-bottom:10px;">
            <a href="{1}"
             target="_blank">View in Google</a>
        </h3>
    """.format(*get_search_links())

    replace_point = '<table class="meta">'
    replacement = new_data + replace_point

    # monkey patch the built-in template.
    debug.TECHNICAL_500_TEMPLATE = debug.TECHNICAL_500_TEMPLATE.replace(
        replace_point,
        replacement,
        1  # replace the first occurence
    )


class DjangoStackoverTraceMiddleware(object):

    def __init__(self):
        if settings.DEBUG:
            _patch_django_debug_view()

    def process_response(self, request, response):
        return response
