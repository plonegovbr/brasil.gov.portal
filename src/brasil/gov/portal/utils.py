# -*- coding: utf-8 -*-
from brasil.gov.portal import _
from six.moves.urllib.parse import urlparse
from zope.interface import Invalid


MESSAGE = _(u'You must use "Title|http://example.org" format to fill each line.')


def validate_list_of_links(value):
    """Check if value is a list of strings that follow the predefined
    format: "Title|http://example.org".
    """
    if not value:
        return True

    for item in value:
        # check string format
        if '|' not in item or item.count('|') > 1:
            raise Invalid(MESSAGE)

        # check if URL is valid
        _, v = item.split('|')
        parsed = urlparse(v.strip())
        if not all([parsed.scheme, parsed.netloc]):
            raise Invalid(MESSAGE)
    return True
