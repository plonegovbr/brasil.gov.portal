# -*- coding: utf-8 -*-
from brasil.gov.portal import _
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedImage
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


def validate_background_image(value):
    """Check if background image has the right dimensions."""
    if not value:
        return True

    filename, data = b64decode_file(value)
    image = NamedImage(data=data, filename=filename)

    width, height = image.getImageSize()
    if width != 1440 or height != 605:
        raise Invalid(_(u'Image should be 1440px width and 605px height.'))

    return True
