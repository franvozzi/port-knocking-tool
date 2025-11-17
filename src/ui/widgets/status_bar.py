import tkinter as tk
from typing import Literal

from utils.constants import COLORS

StatusType = Literal["idle", "connecting", "connected", "error"]


class StatusBar:
    """Barra de estado visual"""

    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.label = tk.Label(
            self.frame, text="Listo para conectar", font=("Arial", 11), fg=COLORS["idle"]
        )
        self.label.pack()

    def update(self, message: str, status: StatusType):
        """Actualiza mensaje y color"""
        color = COLORS.get(status, COLORS["idle"])
        self.label.config(text=message, fg=color)

    def pack(self, **kwargs):
        """Empaqueta el frame"""
        self.frame.pack(**kwargs)
