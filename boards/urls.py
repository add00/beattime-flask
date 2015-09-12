from boards import (
    bp_profile, bp_profile_user,
    bp_board, bp_board_user,
    bp_sprint, bp_sprint_user,
    bp_sticker, bp_sticker_user,
    views,
)
from beattime.utils import register_patterns


profile_rules = [
    (views.ProfileDetail, '/', 'profile-detail'),
    (views.ProfileUpdate, '/update/', 'profile-update'),
    (views.FriendsList, '/friends/', 'friends-list'),
]
register_patterns(bp_profile, profile_rules)
register_patterns(bp_profile_user, profile_rules)

board_rules = [
    (views.BoardDetail, '/<sequence>/', 'board-detail'),
    (views.BoardComments, '/<sequence>/comments/', 'board-comments'),
    (views.BoardCreate, '/new/', 'board-create'),
]
register_patterns(bp_board, board_rules)
register_patterns(bp_board_user, board_rules)

sprint_rules = [
    (views.SprintDetail, '/<number>/', 'sprint-detail'),
    (views.SprintComments, '/<number>/comments/', 'sprint-comments'),
    (views.SprintCreate, '/new/', 'sprint-create'),
]
register_patterns(bp_sprint, sprint_rules)
register_patterns(bp_sprint_user, sprint_rules)

sticker_rules = [
    (views.StickerDetail, '/<prefix>-<sequence>/', 'sticker-detail'),
    (views.StickerUpdate, '/<prefix>-<sequence>/update/', 'sticker-update'),
    (views.StickerCreate, '/new/board/<sequence>/', 'sticker-create-board'),
    (
        views.StickerCreate,
        '/new/board/<sequence>/sprint/<number>/',
        'sticker-create-sprint'
    ),
]
register_patterns(bp_sticker, sticker_rules)
register_patterns(bp_sticker_user, sticker_rules)
