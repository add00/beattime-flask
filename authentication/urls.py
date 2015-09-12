from authentication import bp_authentication, views
from beattime.utils import register_patterns


# bp_authentication.add_url_rule(
#     '/login', view_func=views.LoginView.as_view('login')
# )

# bp_authentication.add_url_rule(
#     '/logout', view_func=views.LogoutView.as_view('logout')
# )

# bp_authentication.add_url_rule(
#     '/new', view_func=views.RegistrationView.as_view('registration')
# )

# bp_authentication.add_url_rule(
#     '/password_change',
#     view_func=views.ChangePasswordView.as_view('password-change')
# )

# bp_authentication.add_url_rule(
#     '/password_reset',
#     view_func=views.PasswordResetView.as_view('password-reset')
# )

# bp_authentication.add_url_rule(
#     '/password_reset/done',
#     view_func=views.PasswordResetDoneView.as_view('password_reset/done')
# )

# bp_authentication.add_url_rule(
#     '/reset/<token>',
#     view_func=views.ResetView.as_view('reset')
# )

# bp_authentication.add_url_rule(
#     '/reset/done',
#     view_func=views.ResetDoneView.as_view('reset-done')
# )

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
