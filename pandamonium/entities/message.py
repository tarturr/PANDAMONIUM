import abc
from datetime import date, datetime

from pandamonium.database import get_db
from pandamonium.entities.data_structures import Entity
from pandamonium.security import max_size_filter


class Message(Entity, abc.ABC):
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
            content=(
                content,
                max_size_filter(1, "Votre message est trop court pour être envoyé.")
            ),
            date_sent=date_sent,
            modified=modified,
            sender_uuid=sender_uuid,
            branch_uuid=branch_uuid,
            response_to_message_uuid=response_to_message_uuid
        )

    @classmethod
    def instant(cls, content: str, sender_uuid: str, branch_uuid: str, response_to_message_uuid: str | None = None):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données.

        :param content: Contenu du message.
        :param sender_uuid: UUID de l'utilisateur ayant envoyé le message.
        :param branch_uuid: UUID de la branche dans lequel le message a été envoyé.
        :param response_to_message_uuid: UUID du message répondu, si le message actuel est une réponse à un autre.

        :rtype Message | None
        :return Instance de la classe Message si les données entrées sont valides, sinon None."""
        db = get_db()
        message = Message(None, content, datetime.now(), False, sender_uuid, branch_uuid, response_to_message_uuid)

        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    message.get_column('uuid'),
                    content,
                    message.get_column('date_sent'),
                    False,
                    sender_uuid,
                    branch_uuid,
                    response_to_message_uuid,
                )
            )

            return message

    @classmethod
    def fetch_by(cls, uuid: str):
        """Crée une instance de Message à partir de son UUID. Ne renvoie rien si le message n'est pas trouvé en base de
        données avec l'UUID fourni.

        :param uuid: UUID du message.

        :rtype Message | None
        :return: Instance de la classe Message si le bamboo existe en base de données avec l'UUID fourni, sinon None."""
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM messages WHERE uuid = %s', (uuid,))
            fetched_message = cursor.fetchone()

            if fetched_message is None:
                return None

            return cls(
                uuid,
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
                        new_content,
                        True,
                        self.get_column('uuid')
                    )
                )
