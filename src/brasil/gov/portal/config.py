# -*- coding: utf-8 -*-

PROJECTNAME = 'brasil.gov.portal'

LOCAL_TIME_FORMAT = '%d/%m/%Y'

TIME_FORMAT = '%Hh%M'

LOCAL_LONG_TIME_FORMAT = '{0} {1}'.format(LOCAL_TIME_FORMAT, TIME_FORMAT)

REDES = [
    {'id': 'facebook',
     'title': 'Facebook',
     'url': 'https://facebook.com/%s'},
    {'id': 'twitter',
     'title': 'Twitter',
     'url': 'https://twitter.com/%s'},
    {'id': 'youtube',
     'title': 'YouTube',
     'url': 'https://youtube.com/%s'},
    {'id': 'flickr',
     'title': 'Flickr',
     'url': 'https://flickr.com/%s'},
    {'id': 'googleplus',
     'title': 'Google+',
     'url': 'https://plus.google.com/%s'},
    {'id': 'slideshare',
     'title': 'Slideshare',
     'url': 'https://slideshare.com/%s'},
    {'id': 'soundcloud',
     'title': 'SoundCloud',
     'url': 'https://soundcloud.com/%s'},
    {'id': 'rss',
     'title': 'RSS',
     'url': '%s'},
    {'id': 'instagram',
     'title': 'Instagram',
     'url': 'https://instagram.com/%s'},
    {'id': 'tumblr',
     'title': 'Thumblr',
     'url': 'https://%s.tumblr.com'},
]

# http://www.tinymce.com/wiki.php/Configuration:formats
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span',
                                          'classes': 'strikethrough',
                                          'exact': 'true'},
                        'underline': {'inline': 'span',
                                      'classes': 'underline',
                                      'exact': 'true'}}
