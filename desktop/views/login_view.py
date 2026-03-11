"""Ventana de inicio de sesión."""

import tkinter as tk
from tkinter import ttk, messagebox

import desktop.api_client as api
from desktop.utils.session import set_session


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Clientes – Iniciar Sesión")
        self.resizable(False, False)
        self._center_window(400, 300)
        self._build_ui()

    def _center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Sistema de Gestión de Clientes", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        ttk.Label(frame, text="Email:").pack(anchor=tk.W)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=35).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Contraseña:").pack(anchor=tk.W)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=35).pack(fill=tk.X, pady=(0, 20))

        self.btn_login = ttk.Button(frame, text="Iniciar Sesión", command=self._on_login)
        self.btn_login.pack(fill=tk.X)

        self.status_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.status_var, foreground="red").pack(pady=(10, 0))

        # Allow pressing Enter to login
        self.bind("<Return>", lambda _e: self._on_login())

    def _on_login(self) -> None:
        email = self.email_var.get().strip()
        password = self.password_var.get()
        if not email or not password:
            self.status_var.set("Por favor, ingrese email y contraseña.")
            return

        self.btn_login.config(state=tk.DISABLED)
        self.status_var.set("Verificando credenciales…")
        self.update_idletasks()

        try:
            resultado = api.login(email, password)
            set_session(resultado["token"], resultado["usuario"])
            self._open_dashboard()
        except __import__("requests").exceptions.ConnectionError:
            self.status_var.set("No se puede conectar al servidor. Verifique que la API esté activa.")
        except __import__("requests").exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 401:
                self.status_var.set("Credenciales inválidas. Intente nuevamente.")
            else:
                self.status_var.set(f"Error del servidor: {exc}")
        except Exception as exc:
            self.status_var.set(f"Error inesperado: {exc}")
        finally:
            self.btn_login.config(state=tk.NORMAL)

    def _open_dashboard(self) -> None:
        from desktop.views.dashboard_view import DashboardView
        self.destroy()
        DashboardView().mainloop()
