# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from zope.interface import implementer
from zope.interface import Interface


class IMinistry(Interface):
    """Explicit marker interface for Ministry."""


@implementer(IMinistry)
class Ministry(Item):
    """Convinience subclass for Ministry portal type."""
