import time

class DummyPortKnocker:
    def __init__(self, target_ip, verbose=True, simulate_success=True):
        self.target_ip = target_ip
        self.verbose = verbose
        self.simulate_success = simulate_success

    def execute_sequence(self, knock_sequence, interval, target_port, progressive_check=True):
        print(f"Simulando port knocking a {self.target_ip}...")
        time.sleep(1)
        if self.simulate_success:
            print("Secuencia de knocks simulada correctamente (puerto abierto).")
            return True
        else:
            print("Secuencia de knocks simulada fallida (puerto cerrado).")
            return False
