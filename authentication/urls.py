from authentication import bp_authentication, views
from beattime.utils import register_patterns


authentication_rules = [
    (views.LoginView, '/login', 'login'),
    (views.LogoutView, '/logout', 'logout'),
    (views.RegistrationView, '/new', 'registration'),
    (views.ChangePasswordView, '/password_change', 'password-change'),
    (views.PasswordResetView, '/password_reset', 'password-reset'),
    (
        views.PasswordResetDoneView,
        '/password_reset/done',
        'password_reset/done'
    ),
    (views.ResetView, '/reset/<token>', 'reset'),
    (views.ResetDoneView, '/reset/done', 'reset-done'),
]
register_patterns(bp_authentication, authentication_rules)
