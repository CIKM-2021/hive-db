from .resources import (
    TestResourceView,
    AccountView
)

routes = [
    ('test', TestResourceView()),
    ('account', AccountView())
]
