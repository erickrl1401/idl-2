"""Formulario para crear o editar un cliente."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

import desktop.api_client as api


class ClienteFormView(tk.Toplevel):
    TIPO_CLIENTE_OPTIONS = ("regular", "premium", "vip")

    def __init__(self, parent, cliente: dict | None = None, on_save: Callable | None = None):
        super().__init__(parent)
        self._cliente = cliente
        self._on_save = on_save
        self._is_edit = cliente is not None
        self.title("Editar Cliente" if self._is_edit else "Nuevo Cliente")
        self.resizable(False, False)
        self.grab_set()
        self._center_window(460, 540)
        self._build_ui()
        if self._is_edit:
            self._populate_fields()

    def _center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Editar Cliente" if self._is_edit else "Nuevo Cliente",
                  font=("Helvetica", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        fields = [
            ("Nombre *:", "nombre"),
            ("Apellido *:", "apellido"),
            ("Email:", "email"),
            ("Teléfono:", "telefono"),
            ("Ciudad:", "ciudad"),
            ("Dirección:", "direccion"),
        ]
        self._vars: dict[str, tk.StringVar] = {}
        for i, (label, key) in enumerate(fields, start=1):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=4)
            var = tk.StringVar()
            self._vars[key] = var
            if key == "direccion":
                entry = tk.Text(frame, width=30, height=3)
                entry.grid(row=i, column=1, sticky=tk.EW, pady=4)
                self._direccion_widget = entry
            else:
                ttk.Entry(frame, textvariable=var, width=30).grid(row=i, column=1, sticky=tk.EW, pady=4)

        # Tipo cliente
        row_tipo = len(fields) + 1
        ttk.Label(frame, text="Tipo Cliente:").grid(row=row_tipo, column=0, sticky=tk.W, pady=4)
        self._tipo_var = tk.StringVar(value="regular")
        ttk.Combobox(
            frame,
            textvariable=self._tipo_var,
            values=self.TIPO_CLIENTE_OPTIONS,
            state="readonly",
            width=28,
        ).grid(row=row_tipo, column=1, sticky=tk.EW, pady=4)

        # Notas
        row_notas = row_tipo + 1
        ttk.Label(frame, text="Notas:").grid(row=row_notas, column=0, sticky=tk.NW, pady=4)
        self._notas_widget = tk.Text(frame, width=30, height=3)
        self._notas_widget.grid(row=row_notas, column=1, sticky=tk.EW, pady=4)

        frame.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row_notas + 1, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text="Guardar", command=self._on_save_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.status_var, foreground="red").grid(
            row=row_notas + 2, column=0, columnspan=2)

    def _populate_fields(self) -> None:
        c = self._cliente
        for key, var in self._vars.items():
            if key != "direccion":
                var.set(c.get(key) or "")
        self._direccion_widget.insert("1.0", c.get("direccion") or "")
        self._tipo_var.set(c.get("tipo_cliente") or "regular")
        self._notas_widget.insert("1.0", c.get("notas") or "")

    def _on_save_click(self) -> None:
        nombre = self._vars["nombre"].get().strip()
        apellido = self._vars["apellido"].get().strip()
        if not nombre or not apellido:
            self.status_var.set("Nombre y Apellido son obligatorios.")
            return

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": self._vars["email"].get().strip() or None,
            "telefono": self._vars["telefono"].get().strip() or None,
            "ciudad": self._vars["ciudad"].get().strip() or None,
            "direccion": self._direccion_widget.get("1.0", tk.END).strip() or None,
            "tipo_cliente": self._tipo_var.get(),
            "notas": self._notas_widget.get("1.0", tk.END).strip() or None,
        }

        try:
            if self._is_edit:
                api.actualizar_cliente(self._cliente["id"], data)
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            else:
                api.crear_cliente(data)
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
            if self._on_save:
                self._on_save()
            self.destroy()
        except Exception as exc:
            self.status_var.set(f"Error: {exc}")
