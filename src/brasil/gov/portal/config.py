# -*- coding: utf-8 -*-

PROJECTNAME = 'brasil.gov.portal'

LOCAL_TIME_FORMAT = '%d/%m/%Y'

TIME_FORMAT = '%Hh%M'

LOCAL_LONG_TIME_FORMAT = '{0} {1}'.format(LOCAL_TIME_FORMAT, TIME_FORMAT)

REDES = [
    {'id': 'facebook',
     'title': 'Facebook',
     'url': 'http://facebook.com/%s'},
    {'id': 'twitter',
     'title': 'Twitter',
     'url': 'https://twitter.com/%s'},
    {'id': 'youtube',
     'title': 'YouTube',
     'url': 'http://youtube.com/%s'},
    {'id': 'flickr',
     'title': 'Flickr',
     'url': 'http://flickr.com/%s'},
    {'id': 'googleplus',
     'title': 'Google+',
     'url': 'http://plus.google.com/%s'},
    {'id': 'slideshare',
     'title': 'Slideshare',
     'url': 'http://slideshare.com/%s'},
    {'id': 'soundcloud',
     'title': 'SoundCloud',
     'url': 'http://soundcloud.com/%s'},
    {'id': 'rss',
     'title': 'RSS',
     'url': '%s'},
    {'id': 'instagram',
     'title': 'Instagram',
     'url': 'http://instagram.com/%s'},
    {'id': 'tumblr',
     'title': 'Thumblr',
     'url': 'http://%s.tumblr.com'},
]

# http://www.tinymce.com/wiki.php/Configuration:formats
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span',
                                          'classes': 'strikethrough',
                                          'exact': 'true'},
                        'underline': {'inline': 'span',
                                      'classes': 'underline',
                                      'exact': 'true'}}
