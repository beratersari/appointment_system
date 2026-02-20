from backend.data_access.db_context import get_connection
from backend.models.entities.appointment import Appointment


class AppointmentRepository:

    def create(self, appointment: Appointment) -> Appointment:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO appointments
                    (company_id, offering_id, customer_name, customer_phone,
                     customer_email, start_date, end_date, created_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    appointment.company_id,
                    appointment.offering_id,
                    appointment.customer_name,
                    appointment.customer_phone,
                    appointment.customer_email,
                    appointment.start_date.isoformat(),
                    appointment.end_date.isoformat(),
                    appointment.created_date.isoformat(),
                    appointment.status.value,
                ),
            )
            connection.commit()
            appointment.id = cursor.lastrowid
            return appointment
        finally:
            connection.close()

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM appointments WHERE id = ?", (appointment_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Appointment.from_row(row)
        finally:
            connection.close()

    def get_all(self) -> list[Appointment]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM appointments")
            rows = cursor.fetchall()
            return [Appointment.from_row(row) for row in rows]
        finally:
            connection.close()

    def get_by_company_id(self, company_id: int) -> list[Appointment]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM appointments WHERE company_id = ?", (company_id,)
            )
            rows = cursor.fetchall()
            return [Appointment.from_row(row) for row in rows]
        finally:
            connection.close()

    def update(self, appointment: Appointment) -> Appointment:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE appointments
                SET company_id = ?, offering_id = ?, customer_name = ?,
                    customer_phone = ?, customer_email = ?, start_date = ?,
                    end_date = ?, status = ?
                WHERE id = ?
                """,
                (
                    appointment.company_id,
                    appointment.offering_id,
                    appointment.customer_name,
                    appointment.customer_phone,
                    appointment.customer_email,
                    appointment.start_date.isoformat(),
                    appointment.end_date.isoformat(),
                    appointment.status.value,
                    appointment.id,
                ),
            )
            connection.commit()
            return appointment
        finally:
            connection.close()

    def delete(self, appointment_id: int) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM appointments WHERE id = ?", (appointment_id,)
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()
