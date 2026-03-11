from api.utils.database import execute_query


class ClienteModel:

    @staticmethod
    def get_all(page: int = 1, per_page: int = 10) -> dict:
        offset = (page - 1) * per_page
        sql_count = "SELECT COUNT(*) AS total FROM clientes WHERE activo = TRUE"
        total_row = execute_query(sql_count, fetch_one=True)
        total = total_row["total"] if total_row else 0

        sql = """
            SELECT c.*, u.nombre AS creado_por_nombre
            FROM clientes c
            LEFT JOIN usuarios u ON c.created_by = u.id
            WHERE c.activo = TRUE
            ORDER BY c.created_at DESC
            LIMIT %s OFFSET %s
        """
        clientes = execute_query(sql, (per_page, offset), fetch_all=True)
        return {"clientes": clientes or [], "total": total, "page": page, "per_page": per_page}

    @staticmethod
    def get_by_id(cliente_id: int) -> dict | None:
        sql = """
            SELECT c.*, u.nombre AS creado_por_nombre
            FROM clientes c
            LEFT JOIN usuarios u ON c.created_by = u.id
            WHERE c.id = %s AND c.activo = TRUE
        """
        return execute_query(sql, (cliente_id,), fetch_one=True)

    @staticmethod
    def search(query: str, page: int = 1, per_page: int = 10) -> dict:
        like = f"%{query}%"
        offset = (page - 1) * per_page

        sql_count = """
            SELECT COUNT(*) AS total FROM clientes
            WHERE activo = TRUE
              AND (nombre LIKE %s OR apellido LIKE %s OR email LIKE %s OR telefono LIKE %s OR ciudad LIKE %s)
        """
        total_row = execute_query(sql_count, (like, like, like, like, like), fetch_one=True)
        total = total_row["total"] if total_row else 0

        sql = """
            SELECT c.*, u.nombre AS creado_por_nombre
            FROM clientes c
            LEFT JOIN usuarios u ON c.created_by = u.id
            WHERE c.activo = TRUE
              AND (c.nombre LIKE %s OR c.apellido LIKE %s OR c.email LIKE %s
                   OR c.telefono LIKE %s OR c.ciudad LIKE %s)
            ORDER BY c.nombre ASC
            LIMIT %s OFFSET %s
        """
        clientes = execute_query(sql, (like, like, like, like, like, per_page, offset), fetch_all=True)
        return {"clientes": clientes or [], "total": total, "page": page, "per_page": per_page}

    @staticmethod
    def create(data: dict, created_by: int) -> int:
        sql = """
            INSERT INTO clientes
                (nombre, apellido, email, telefono, direccion, ciudad, tipo_cliente, notas, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return execute_query(
            sql,
            (
                data["nombre"],
                data["apellido"],
                data.get("email"),
                data.get("telefono"),
                data.get("direccion"),
                data.get("ciudad"),
                data.get("tipo_cliente", "regular"),
                data.get("notas"),
                created_by,
            ),
            commit=True,
        )

    @staticmethod
    def update(cliente_id: int, data: dict) -> bool:
        # Build the SET clause from a fixed allowlist of safe column names.
        # The allowlist prevents SQL injection even if additional keys are added later.
        fields = []
        values = []
        allowed = ["nombre", "apellido", "email", "telefono", "direccion", "ciudad", "tipo_cliente", "notas"]
        for field in allowed:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])
        if not fields:
            return False
        values.append(cliente_id)
        sql = f"UPDATE clientes SET {', '.join(fields)} WHERE id = %s AND activo = TRUE"
        execute_query(sql, tuple(values), commit=True)
        return True

    @staticmethod
    def delete(cliente_id: int) -> bool:
        sql = "UPDATE clientes SET activo = FALSE WHERE id = %s"
        execute_query(sql, (cliente_id,), commit=True)
        return True
