import json

import unittest
from flask import url_for, request
from beattime import create_app, db
from boards.models import Desk, Board, Sticker, Label
from profiles.models import Profile


class StickerAPITestCase(unittest.TestCase):

    fixtures = ['boards/fixtures/fixture.json']

    def setUp(self):

        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        user = Profile(
            email='test@email.com',
            username='u1',
            password='u1',
            display_name='u1',
            motivation_quote='u1'
        )
        db.session.add(user)
        db.session.commit()

        desk = Desk(
            author=user.id,
            owner_id=user.id,
            desk_slug='test'
        )
        db.session.add(desk)
        db.session.commit()

        board = Board(
            author=user.id,
            desk_id=desk.id,
            title='test',
            sequence=1,
            prefix='test'
        )
        db.session.add(board)
        db.session.commit()

        label = Label(
            color='#fff',
            css_class='OPEN',
            status='OPEN'
        )
        db.session.add(label)
        db.session.commit()

        sticker = Sticker(
            author=user.id,
            board_id=board.id,
            caption='test',
            description='test',
            label_id=label.id,
            sequence=1
        )
        db.session.add(sticker)
        db.session.commit()

        self.client.post(
            url_for('bp_authentication.login', username='u1', password='u1')
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_sticker_api(self):
        request.view_args.update({'username': 'u1'})
        response = self.client.get(
            url_for('bp_profile.api-stickers', username='u1'),
        )
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(
            response_json,
            {
                u'1': {
                    u'caption': u'test',
                    u'description': u'test',
                    u'status': u'OPEN'
                }
            }
        )
