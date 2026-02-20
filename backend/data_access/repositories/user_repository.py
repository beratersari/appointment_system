from backend.data_access.db_context import get_connection
from backend.models.entities.user import User


class UserRepository:

    def create(self, user: User) -> User:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO users
                    (username, password_hash, email, role, company_id, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user.username,
                    user.password_hash,
                    user.email,
                    user.role.value,
                    user.company_id,
                    user.created_date.isoformat(),
                ),
            )
            connection.commit()
            user.id = cursor.lastrowid
            return user
        finally:
            connection.close()

    def get_by_username(self, username: str) -> User | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return User.from_row(row)
        finally:
            connection.close()

    def get_by_id(self, user_id: int) -> User | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return User.from_row(row)
        finally:
            connection.close()

    def get_by_email(self, email: str) -> User | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row is None:
                return None
            return User.from_row(row)
        finally:
            connection.close()
