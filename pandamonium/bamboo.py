import flask as fk

from datetime import datetime

import mysql.connector.cursor as cursor

from pandamonium.database import get_db
from pandamonium.security import check_password, date_from_string, date_to_string, fill_requirements, \
    set_security_error

from uuid import uuid4


class Bamboo:
    """Classe représentant un serveur unique du réseau social.
    Par "bambou", nous parlons d'un endroit virtuel créé sur notre réseau social pour discuter de façon communautaire.
    Différentes "branches" de discussion peuvent être créése, des rôles et permissions peuvent être
    attribués aux différents membres par le créateur ou les administrateurs du bambou."""

    def __init__(
            self,
            bamboo_uuid: str,
            name: str,
            creator: str,
            creation_time: str,
            pic: str,
            banner: str
    ):
        self.uuid = bamboo_uuid

        db = get_db()
        with db.cursor() as curs:
            curs.execute(
                'SELECT name, creation_time, uuid_1 FROM bamboos WHERE uuid = %',
                self.uuid
            )
            bamboo = curs.fetchone()
            self.name = bamboo[0]
            self.creation_time = bamboo[1]
            self.creator = bamboo[2]

    def create(self, name):
        self.uuid = uuid4()
        self.name = name
        self.creator = fk.session['username']
        self.creation_time = datetime.now()

        db = get_db()
        db.cursor().execute(
            'INSERT INTO bamboos(uuid, name, creation_time, creator) VALUES (%s, %s, %s, %s)',
            (self.uuid, self.name, self.creation_time, self.creator)
        )

    def update(
            self,
            name: str,
    ):
        if self.name != name:
            self.name = name

        db = get_db()
        db.cursor().execute(
            'UPDATE servers SET name = %s, pic = %s, banner = %s WHERE id = %s',
            (self.name, self.pic, self.banner, self.uuid)
        )
