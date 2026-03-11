"""Panel principal (dashboard) de la aplicación de escritorio."""

import tkinter as tk
from tkinter import ttk, messagebox

from desktop.utils.session import get_usuario, clear_session


class DashboardView(tk.Tk):
    def __init__(self):
        super().__init__()
        usuario = get_usuario() or {}
        self.title(f"Sistema de Gestión de Clientes – {usuario.get('nombre', '')}")
        self.geometry("900x600")
        self._center_window(900, 600)
        self._build_ui()

    def _center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        # Top bar
        top_bar = ttk.Frame(self, padding=(10, 5))
        top_bar.pack(fill=tk.X, side=tk.TOP)

        usuario = get_usuario() or {}
        ttk.Label(
            top_bar,
            text=f"Bienvenido, {usuario.get('nombre', '')} ({usuario.get('rol', '')})",
            font=("Helvetica", 11),
        ).pack(side=tk.LEFT)

        ttk.Button(top_bar, text="Cerrar Sesión", command=self._logout).pack(side=tk.RIGHT)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # Sidebar
        sidebar = ttk.Frame(self, padding=10, width=180)
        sidebar.pack(fill=tk.Y, side=tk.LEFT)
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="Menú", font=("Helvetica", 12, "bold")).pack(pady=(0, 10))
        ttk.Button(sidebar, text="📋 Clientes", width=18, command=self._show_clientes).pack(fill=tk.X, pady=3)

        ttk.Separator(self, orient=tk.VERTICAL).pack(fill=tk.Y, side=tk.LEFT)

        # Main content area
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self._show_clientes()

    def _show_clientes(self) -> None:
        for w in self.content_frame.winfo_children():
            w.destroy()
        from desktop.views.cliente_list import ClienteListView
        ClienteListView(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def _logout(self) -> None:
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            clear_session()
            from desktop.views.login_view import LoginView
            self.destroy()
            LoginView().mainloop()
