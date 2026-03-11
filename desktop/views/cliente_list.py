"""Vista de lista/tabla de clientes con búsqueda y paginación."""

import tkinter as tk
from tkinter import ttk, messagebox

import desktop.api_client as api


class ClienteListView(ttk.Frame):
    PAGE_SIZE = 10

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._page = 1
        self._total = 0
        self._search_query = ""
        self._build_ui()
        self._load_clientes()

    def _build_ui(self) -> None:
        # Title + buttons row
        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(top, text="Gestión de Clientes", font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="+ Nuevo Cliente", command=self._new_cliente).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top, text="🔄 Actualizar", command=self._refresh).pack(side=tk.RIGHT)

        # Search bar
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT)
        search_entry.bind("<Return>", lambda _e: self._on_search())
        ttk.Button(search_frame, text="🔍 Buscar", command=self._on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="✖ Limpiar", command=self._clear_search).pack(side=tk.LEFT)

        # Table
        cols = ("id", "nombre", "apellido", "email", "telefono", "ciudad", "tipo_cliente")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        headers = {
            "id": ("ID", 45),
            "nombre": ("Nombre", 120),
            "apellido": ("Apellido", 120),
            "email": ("Email", 170),
            "telefono": ("Teléfono", 100),
            "ciudad": ("Ciudad", 100),
            "tipo_cliente": ("Tipo", 80),
        }
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor=tk.W)

        scroll_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)

        self.tree.bind("<Double-1>", lambda _e: self._on_edit())

        # Bottom bar: pagination + actions
        bottom = ttk.Frame(self)
        bottom.pack(fill=tk.X, pady=(8, 0))

        self.status_var = tk.StringVar()
        ttk.Label(bottom, textvariable=self.status_var).pack(side=tk.LEFT)

        ttk.Button(bottom, text="Eliminar", command=self._on_delete).pack(side=tk.RIGHT, padx=5)
        ttk.Button(bottom, text="Editar", command=self._on_edit).pack(side=tk.RIGHT, padx=5)

        # Pagination
        pag_frame = ttk.Frame(self)
        pag_frame.pack(fill=tk.X, pady=(4, 0))

        self.btn_prev = ttk.Button(pag_frame, text="◀ Anterior", command=self._prev_page)
        self.btn_prev.pack(side=tk.LEFT, padx=2)
        self.page_label = ttk.Label(pag_frame, text="Página 1")
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.btn_next = ttk.Button(pag_frame, text="Siguiente ▶", command=self._next_page)
        self.btn_next.pack(side=tk.LEFT, padx=2)

    # -----------------------------------------------------------------------
    # Data loading
    # -----------------------------------------------------------------------

    def _load_clientes(self) -> None:
        try:
            if self._search_query:
                resultado = api.buscar_clientes(self._search_query, self._page, self.PAGE_SIZE)
            else:
                resultado = api.get_clientes(self._page, self.PAGE_SIZE)
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes:\n{exc}")
            return

        self._total = resultado.get("total", 0)
        self.tree.delete(*self.tree.get_children())
        for c in resultado.get("clientes", []):
            self.tree.insert(
                "", tk.END,
                iid=str(c["id"]),
                values=(
                    c["id"],
                    c.get("nombre", ""),
                    c.get("apellido", ""),
                    c.get("email", ""),
                    c.get("telefono", ""),
                    c.get("ciudad", ""),
                    c.get("tipo_cliente", ""),
                ),
            )

        total_pages = max(1, (self._total + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        self.page_label.config(text=f"Página {self._page} de {total_pages}")
        self.status_var.set(f"{self._total} cliente(s) encontrado(s)")
        self.btn_prev.config(state=tk.NORMAL if self._page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self._page < total_pages else tk.DISABLED)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _refresh(self) -> None:
        self._load_clientes()

    def _on_search(self) -> None:
        self._search_query = self.search_var.get().strip()
        self._page = 1
        self._load_clientes()

    def _clear_search(self) -> None:
        self.search_var.set("")
        self._search_query = ""
        self._page = 1
        self._load_clientes()

    def _prev_page(self) -> None:
        if self._page > 1:
            self._page -= 1
            self._load_clientes()

    def _next_page(self) -> None:
        total_pages = max(1, (self._total + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        if self._page < total_pages:
            self._page += 1
            self._load_clientes()

    def _new_cliente(self) -> None:
        from desktop.views.cliente_form import ClienteFormView
        ClienteFormView(self.winfo_toplevel(), on_save=self._refresh)

    def _on_edit(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar", "Seleccione un cliente para editar.")
            return
        cliente_id = int(selected[0])
        try:
            data = api.get_cliente(cliente_id)
            cliente = data["cliente"]
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return
        from desktop.views.cliente_form import ClienteFormView
        ClienteFormView(self.winfo_toplevel(), cliente=cliente, on_save=self._refresh)

    def _on_delete(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar", "Seleccione un cliente para eliminar.")
            return
        cliente_id = int(selected[0])
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el cliente con ID {cliente_id}?"):
            return
        try:
            api.eliminar_cliente(cliente_id)
            self._load_clientes()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
