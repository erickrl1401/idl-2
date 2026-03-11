"""Punto de entrada de la aplicación de escritorio."""

import sys
import os

# Ensure the project root is in sys.path so 'desktop' and 'api' packages resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desktop.views.login_view import LoginView


def main() -> None:
    app = LoginView()
    app.mainloop()


if __name__ == "__main__":
    main()
