import flask as fk

from datetime import datetime

import mysql.connector.cursor as cursor

from pandamonium.database import get_db, new_id
from pandamonium.security import check_password, date_from_string, date_to_string, fill_requirements, \
    set_security_error


class Bamboo:
    """Classe représentant un serveur unique du réseau social.
    Par "bambou", nous parlons d'un endroit virtuel créé sur notre réseau social pour discuter de façon communautaire.
    Différentes "branches" de discussion peuvent être créése, des rôles et permissions peuvent être
    attribués aux différents membres par le créateur ou les administrateurs du bambou."""

    def __init__(
            self,
            server_id: str,
            name: str,
            creator: str,
            creation_time: str,
            pic: str,
            banner: str
    ):
        self.id = server_id
        self.name = name
        self.creator = creator
        self.creation_time = creation_time
        self.pic = pic
        self.banner = banner

    def create(self, name):
        self.id = new_id('bamboos', 'id')
        self.name = name
        self.creator = fk.session['username']
        self.creation_time = datetime.now()
        self.pic = None
        self.banner = None

        get_db()
        db.cursor.execute()



    def change_settings(
            self,
            name: str,
            pic: str,
            banner: str
    ):
        if self.name != name:
            self.name = name
        if self.pic != pic:
            self.pic = pic
        if self.banner != banner:
            self.banner = banner

        db = get_db()

        db.cursor().execute(
            'UPDATE servers SET name = %s, pic = %s, banner = %s WHERE id = %s',
            (self.name, self.pic, self.banner, self.id)
        )
