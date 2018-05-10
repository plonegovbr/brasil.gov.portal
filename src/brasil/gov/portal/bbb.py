# -*- coding: utf-8 -*-
"""
Módulo criado inicialmente para resolver o problema da browserlayer de
collective.oembed e plone.app.collection versão 2.0b5 que registram browser
layers mas foram (serão) removidos em versões posteriores do brasil.gov.portal.

Mais informações:

https://github.com/plonegovbr/portalpadrao.release/issues/10

Esse módulo pode ser removido quando brasil.gov.portal for 2.x. Favor informar
no CHANGES.rst essa informação quando remover esse módulo.
"""
from brasil.gov.portal.logger import logger
from zope.interface import Interface

import new
import sys


modules = [
    'collective.oembed.interfaces.OEmbedLayer',
    'plone.app.collection.interfaces.IPloneAppCollectionLayer',
]


def alias_module(name, target):
    parts = name.split('.')
    i = 0
    module = None
    while i < len(parts) - 1:
        i += 1
        module_name = '.'.join(parts[:i])
        try:
            __import__(module_name)
        except ImportError:
            new_module = new.module(module_name)
            sys.modules[module_name] = new_module
            if module is not None:
                setattr(module, parts[i - 1], new_module)
        module = sys.modules[module_name]

    setattr(module, parts[-1], target)
    # also make sure sys.modules is updated
    sys.modules[module_name + '.' + parts[-1]] = target


for module in modules:
    alias_module(module, Interface)

logger.warning(
    'Criando as classes fake para retirar a layer'
    ' do collective.oembed e plone.app.collection'
    ' evitando pickling errors entre upgradesteps')
