import bcrypt
from api.utils.database import execute_query


class UsuarioModel:

    @staticmethod
    def get_by_email(email: str) -> dict | None:
        sql = "SELECT * FROM usuarios WHERE email = %s AND activo = TRUE"
        return execute_query(sql, (email,), fetch_one=True)

    @staticmethod
    def get_by_id(usuario_id: int) -> dict | None:
        sql = "SELECT id, nombre, email, rol, activo, created_at FROM usuarios WHERE id = %s"
        return execute_query(sql, (usuario_id,), fetch_one=True)

    @staticmethod
    def create(nombre: str, email: str, password: str, rol: str = "empleado") -> int:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
        sql = """
            INSERT INTO usuarios (nombre, email, password_hash, rol)
            VALUES (%s, %s, %s, %s)
        """
        return execute_query(sql, (nombre, email, password_hash, rol), commit=True)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
