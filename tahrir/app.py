from pyramid.security import Allow
from pyramid.security import Everyone

import tahrir_api.model as m


class AssertionApp(object):
    __name__ = 'assertions'

    def __init__(self, badge):
        self.badge = badge

    def __getitem__(self, key):
        return m.Assertion.query.filter_by(
            recipient=key,
            badge=self.badge,
        ).one()


class InvitationApp(object):
    __name__ = 'invitations'

    def __getitem__(self, key):
        resource = m.Invitation.query.filter(
            m.Invitation.id==key,
        ).one()
        resource.__parent__ = self
        resource.__name__ = resource.id
        return resource


class RootApp(object):
    __name__ = None
    __parent__ = None

    def __getitem__(self, key):
        if key == 'assertions':
            return self

        if key == 'invitations':
            resource = InvitationApp()
            resource.__parent__ = self
            return resource

        # else

        try:
            badge = m.Badge.query.filter_by(id=key).one()
            return AssertionApp(badge=badge)
        except:
            return self


def get_root(request):
    return RootApp()
