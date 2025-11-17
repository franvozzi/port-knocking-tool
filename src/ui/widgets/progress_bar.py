from tkinter import ttk


class ConnectionProgress:
    """Barra de progreso de conexión"""

    def __init__(self, parent):
        self.progress = ttk.Progressbar(parent, orient="horizontal", length=300, mode="determinate")
        self.progress["maximum"] = 100
        self.progress["value"] = 0

    def set_progress(self, value: int):
        """Establece progreso (0-100)"""
        self.progress["value"] = min(100, max(0, value))

    def reset(self):
        """Resetea progreso"""
        self.progress["value"] = 0

    def pack(self, **kwargs):
        """Empaqueta el widget"""
        self.progress.pack(**kwargs)
