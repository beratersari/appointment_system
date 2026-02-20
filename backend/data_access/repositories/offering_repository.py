from backend.data_access.db_context import get_connection
from backend.models.entities.offering import Offering


class OfferingRepository:

    def create(self, offering: Offering) -> Offering:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO offerings
                    (company_id, description, is_open, created_date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    offering.company_id,
                    offering.description,
                    int(offering.is_open),
                    offering.created_date.isoformat(),
                ),
            )
            connection.commit()
            offering.id = cursor.lastrowid
            return offering
        finally:
            connection.close()

    def get_by_id(self, offering_id: int) -> Offering | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM offerings WHERE id = ?", (offering_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Offering.from_row(row)
        finally:
            connection.close()

    def get_by_company_id(self, company_id: int) -> list[Offering]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM offerings WHERE company_id = ?", (company_id,)
            )
            rows = cursor.fetchall()
            return [Offering.from_row(row) for row in rows]
        finally:
            connection.close()

    def get_open_by_company_id(self, company_id: int) -> list[Offering]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM offerings WHERE company_id = ? AND is_open = 1",
                (company_id,),
            )
            rows = cursor.fetchall()
            return [Offering.from_row(row) for row in rows]
        finally:
            connection.close()

    def update(self, offering: Offering) -> Offering:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE offerings
                SET description = ?, is_open = ?
                WHERE id = ?
                """,
                (
                    offering.description,
                    int(offering.is_open),
                    offering.id,
                ),
            )
            connection.commit()
            return offering
        finally:
            connection.close()
