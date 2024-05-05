from abc import ABC
from datetime import date, datetime

from pandamonium.database import Entity, get_db
from pandamonium.security import max_size_filter


class Message(Entity, ABC):
    """Classe représentant un message envoyé dans la branche d'un bamboo."""

    def __init__(self,
                 uuid: str | None,
                 content: str | None,
                 date_sent: date | None,
                 modified: bool | None,
                 sender_uuid: str | None,
                 branch_uuid: str | None,
                 response_to_message_uuid: str | None = None):
        """Constructeur de la classe Message.

        :param uuid: UUID du message.
        :param content: Contenu du message.
        :param date_sent: Date d'envoi du message.
        :param modified: Message modifié ou non.
        :param sender_uuid: UUID de l'utilisateur ayant envoyé le message.
        :param branch_uuid: UUID de la branche dans lequel le message a été envoyé.
        :param response_to_message_uuid: UUID du message répondu, si le message actuel est une réponse à un autre."""
        super().__init__(
            'message',
            uuid,
            content=(content, max_size_filter(1, "Votre message est trop court pour être envoyé.")),
            date_sent=date_sent,
            modified=modified,
            sender_uuid=sender_uuid,
            branch_uuid=branch_uuid,
            response_to_message_uuid=response_to_message_uuid
        )

    @classmethod
    def instant(cls, content: str, sender_uuid: str, branch_uuid: str, response_to_message_uuid: str | None):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données.

        :param content: Contenu du message.
        :param sender_uuid: UUID de l'utilisateur ayant envoyé le message.
        :param branch_uuid: UUID de la branche dans lequel le message a été envoyé.
        :param response_to_message_uuid: UUID du message répondu, si le message actuel est une réponse à un autre."""
        db = get_db()
        message = Message(None, content, datetime.now(), False, sender_uuid, branch_uuid, response_to_message_uuid)

        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    message.get_column('uuid').value,
                    message.get_column('content').value,
                    message.get_column('date_sent').value,
                    message.get_column('modified').value,
                    message.get_column('sender_uuid').value,
                    message.get_column('branch_uuid').value,
                    message.get_column('response_to_message_uuid').value,
                )
            )

            return message

    @classmethod
    def fetch_by(cls, uuid: str):
        """Permet d'obtenir un message via son UUID.

        :param uuid: UUID du message."""
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM messages WHERE uuid = %s', [uuid])
            fetched_message = cursor.fetchone()

            return cls(
                fetched_message['uuid'],
                fetched_message['content'],
                fetched_message['date_sent'],
                fetched_message['modified'],
                fetched_message['sender_uuid'],
                fetched_message['branch_uuid'],
                fetched_message['response_to_message_uuid']
            )

    def _update(self, new_content: str):
        """Met à jour le contenu du message actuel. Il devient alors modifié.

        :param new_content: Nouveau contenu du message."""
        self.set_column('content', new_content)

        if self.valid:
            self.set_column('modified', True)

            with get_db().cursor() as cursor:
                cursor.execute(
                    'UPDATE messages SET content = %s, modified = %s WHERE uuid = %s',
                    (
                        self.get_column('content').value,
                        self.get_column('modified').value,
                        self.get_column('uuid').value
                    )
                )
