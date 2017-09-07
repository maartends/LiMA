# -*- coding: utf-8 -*-
from formalchemy import forms
from formalchemy import tables
from pyramid_formalchemy.views import ModelView as P_ModelView
from fa.jquery.pyramid import ModelView
from pyramid_formalchemy import actions, events
from zope.interface import alsoProvides
import zope.component.event

# standard form buttons (from pyramid_formalchemy.actions)
# TODO: should not be re-defined!
save = actions.UIButton(
        id='save',
        content='Save',
        permission='edit',
        icon='ui-icon-check',
        attrs=dict(onclick="jQuery(this).parents('form').submit();"),
        )

delete = actions.UIButton(
        id='delete',
        content='Delete',
        permission='delete',
        state='ui-state-error',
        icon='ui-icon-trash',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                      "f.attr('action', window.location.href.replace('/edit', '/delete'));"
                      "f.submit();")),
        )

cancel = actions.UIButton(
        id='cancel',
        content='Cancel',
        permission='view',
        icon='ui-icon-circle-arrow-w',
        attrs=dict(href="request.fa_url(request.model_name)"),
        )
# custom form buttons
copy = actions.UIButton(
        id='copy',
        content='Copy (werkt nog niet :-) )',
        permission='new',
        icon='ui-icon-circle-plus',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                      "f.attr('action', window.location.href.replace('/edit', '/copy'));"
                      "f.submit();")),
        )

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

# subclass ModelView class from pyramid_formalchemy
class MM_ModelView(ModelView):
    """
    blabalabl
    """
    #~ @actions.action()
    #~ def copy(self):
        #~ id = self.request.model_id
        #~ fs = self.get_fieldset(suffix='Copy', id=id)
#~
        #~ event = events.BeforeRenderEvent(self.request.model_instance, self.request, fs=fs)
        #~ alsoProvides(event, events.IBeforeEditRenderEvent)
        #~ zope.component.event.objectEventNotify(event)
#~
        #~ return self.render(fs=fs, id=id)

    # keep default action categorie and add the custom_actions categorie
    # see
    actions_categories = ('buttons', 'mm_edit_buttons')
    # update the default actions for all models
    defaults_actions = actions.defaults_actions.copy()
    # fit in copy button with the default buttons
    defaults_actions.update(edit_buttons=actions.Actions(save, delete, copy, cancel))

class P_ModelView(P_ModelView):
    pass
