import time


def main():
    print("Simulando conexión OpenVPN (dummy)...")
    time.sleep(2)
    print("Dummy: Conexión establecida.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Dummy OpenVPN finalizado.")


if __name__ == "__main__":
    main()
