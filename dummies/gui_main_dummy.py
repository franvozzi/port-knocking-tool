import tkinter as tk
from tkinter import messagebox
import threading
import time
import subprocess
import sys
from dummy_knocker import DummyPortKnocker


class VPNConnectDummyGUI:
    def __init__(self, simulate_success=True):
        self.simulate_success = simulate_success
        self.window = tk.Tk()
        self.window.title("Conexión VPN Dummy")
        self.window.geometry("450x250")
        self.window.resizable(False, False)

        self.status_label = tk.Label(
            self.window, text="Listo para conectar (dummy)", font=("Arial", 11), fg="#666"
        )
        self.status_label.pack(pady=20)

        self.connect_btn = tk.Button(
            self.window,
            text="Conectar",
            command=self.start_connection,
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
            cursor="hand2",
        )
        self.connect_btn.pack(pady=15)

        self.disconnect_btn = tk.Button(
            self.window,
            text="Desconectar",
            command=self.disconnect_vpn,
            font=("Arial", 10),
            state="disabled",
            width=18,
        )
        self.disconnect_btn.pack(pady=5)

    def update_status(self, message, color="#666"):
        self.status_label.config(text=message, fg=color)
        self.window.update()

    def start_connection(self):
        self.connect_btn.config(state="disabled")
        thread = threading.Thread(target=self.do_connection, daemon=True)
        thread.start()

    def do_connection(self):
        try:
            self.update_status("Simulando port knocking...", "#FF9800")
            knocker = DummyPortKnocker("203.0.113.10", simulate_success=self.simulate_success)
            success = knocker.execute_sequence([[7000, "tcp"], [8000, "tcp"]], 0.5, 1194)
            if not success:
                self.update_status("✗ Puerto cerrado (dummy)", "#F44336")
                messagebox.showerror(
                    "Error de Conexión", "Dummy: Port knocking fallido (puerto cerrado)."
                )
                self.connect_btn.config(state="normal")
                return

            self.update_status("Simulando conexión VPN...", "#2196F3")
            subprocess.Popen([sys.executable, "openvpn_dummy.py"])
            time.sleep(2)
            self.update_status("✓ Conectado exitosamente (dummy)", "#4CAF50")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
        except Exception as e:
            self.update_status("✗ Error de conexión (dummy)", "#F44336")
            messagebox.showerror("Error de Conexión", f"Dummy: {e}")
            self.connect_btn.config(state="normal")

    def disconnect_vpn(self):
        self.update_status("Desconectado (dummy)", "#666")
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # Cambia True a False para simular puerto cerrado
    app = VPNConnectDummyGUI(simulate_success=True)
    app.run()
