# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from zope.interface import implementer
from zope.interface import Interface


class IInfographic(Interface):
    """Explicit marker interface for Infographic."""


@implementer(IInfographic)
class Infographic(Item):
    """Convinience subclass for Infographic portal type."""
