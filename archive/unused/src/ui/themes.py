from typing import Dict

THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "accent": "#4CAF50",
        "error": "#F44336",
        "warning": "#FF9800",
        "info": "#2196F3"
    },
    "dark": {
        "bg": "#1E1E1E",
        "fg": "#FFFFFF",
        "accent": "#00BCD4",
        "error": "#FF5252",
        "warning": "#FFC107",
        "info": "#42A5F5"
    },
    "corporate": {
        "bg": "#F5F5F5",
        "fg": "#333333",
        "accent": "#0066CC",
        "error": "#D32F2F",
        "warning": "#F57C00",
        "info": "#1976D2"
    }
}

class ThemeManager:
    """Gestor de temas de la interfaz"""
    
    def __init__(self, window, theme_name: str = "light"):
        self.window = window
        self.current_theme = theme_name
        self.apply_theme(theme_name)
    
    def apply_theme(self, theme_name: str):
        """Aplica tema a la ventana"""
        if theme_name not in THEMES:
            theme_name = "light"
        
        theme = THEMES[theme_name]
        self.window.configure(bg=theme["bg"])
        self.current_theme = theme_name
    
    def get_color(self, color_type: str) -> str:
        """Obtiene color del tema actual"""
        theme = THEMES[self.current_theme]
        return theme.get(color_type, "#000000")
