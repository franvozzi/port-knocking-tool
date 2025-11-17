import unittest
from unittest.mock import Mock, patch
import socket
import threading
import time
from src.core.port_knocker import PortKnocker


class TestPortKnocker(unittest.TestCase):
    """Tests unitarios con mocks"""

    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.target_ip = "192.168.88.1"
        self.knocker = PortKnocker()

    @patch("socket.socket")
    def test_tcp_knock_success(self, mock_socket):
        """Test de knock TCP exitoso"""
        # Configurar el mock
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock_instance

        # Ejecutar
        result = self.knocker._knock_port(self.target_ip, 8881, "tcp")

        # Verificar
        self.assertTrue(result)
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock_instance.connect_ex.assert_called_once_with((self.target_ip, 8881))
        mock_sock_instance.close.assert_called_once()

    @patch("socket.socket")
    def test_udp_knock_success(self, mock_socket):
        """Test de knock UDP exitoso"""
        # Configurar el mock
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # Ejecutar
        result = self.knocker._knock_port(self.target_ip, 5555, "udp")

        # Verificar
        self.assertTrue(result)
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
        mock_sock_instance.sendto.assert_called_once_with(b"", (self.target_ip, 5555))
        mock_sock_instance.close.assert_called_once()

    @patch("socket.socket")
    def test_tcp_knock_failure(self, mock_socket):
        """Test de knock TCP con error"""
        # Configurar mock para lanzar excepción
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.side_effect = socket.error("Connection refused")
        mock_socket.return_value = mock_sock_instance

        # Ejecutar
        result = self.knocker._knock_port(self.target_ip, 8881, "tcp")

        # Verificar que retorna False
        self.assertFalse(result)

    @patch("time.sleep")
    @patch("socket.socket")
    def test_execute_sequence_mixed(self, mock_socket, mock_sleep):
        """Test de secuencia con protocolos mixtos"""
        # Configurar mock
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock_instance

        # Secuencia de test
        knock_sequence = [(8881, "tcp"), (5555, "udp"), (2222, "tcp")]
        interval = 0.5

        # Ejecutar
        self.knocker.execute_sequence(self.target_ip, knock_sequence, interval, 2222)

        # Verificar: 3 sockets creados para los knocks, más las llamadas de verificación
        # El número exacto puede variar, así que verificamos que sea al menos 3
        self.assertGreaterEqual(mock_socket.call_count, 3)

        # Verificar: 2 sleeps (entre 3 knocks)
        self.assertGreaterEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_called_with(interval)

    @patch("socket.socket")
    def test_execute_sequence_all_tcp(self, mock_socket):
        """Test de secuencia solo TCP"""
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock_instance

        knock_sequence = [(8881, "tcp"), (5555, "tcp")]

        self.knocker.execute_sequence(self.target_ip, knock_sequence, 0.1, 2222)

        # Verificar que se usó SOCK_STREAM para ambos
        calls = mock_socket.call_args_list
        for call in calls:
            self.assertEqual(call[0], (socket.AF_INET, socket.SOCK_STREAM))


class TestPortKnockerIntegration(unittest.TestCase):
    """Tests de integración con servidor simulado"""

    def setUp(self):
        """Configurar servidor simulado MikroTik"""
        self.knock_ports = [8881, 5555, 2222, 9999, 7777]
        self.protected_service_port = 22222  # Cambiar a puerto alto para evitar conflictos
        self.knock_sequence_received = []
        self.access_granted = False
        self.servers_running = True
        self.server_threads = []
        self.knock_sockets = []
        self.protected_socket = None

        # Iniciar servidores de knock
        for port in self.knock_ports:
            thread = threading.Thread(target=self._knock_server, args=(port,), daemon=True)
            thread.start()
            self.server_threads.append(thread)

        # Iniciar servidor del servicio protegido
        protected_thread = threading.Thread(target=self._protected_service_server, daemon=True)
        protected_thread.start()
        self.server_threads.append(protected_thread)

        # Esperar a que los servidores inicien
        time.sleep(0.3)

    def tearDown(self):
        """Limpiar servidores"""
        self.servers_running = False
        time.sleep(0.2)

        # Cerrar sockets explícitamente
        for sock in self.knock_sockets:
            try:
                sock.close()
            except:
                pass

        if self.protected_socket:
            try:
                self.protected_socket.close()
            except:
                pass

    def _knock_server(self, port):
        """Servidor que escucha knocks en un puerto específico"""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", port))
            sock.listen(5)
            sock.settimeout(0.5)
            self.knock_sockets.append(sock)

            while self.servers_running:
                try:
                    conn, addr = sock.accept()
                    self.knock_sequence_received.append(port)
                    print(f"✓ Knock recibido en puerto {port}")

                    # Si recibimos los 5 knocks en orden, otorgar acceso
                    if self.knock_sequence_received == self.knock_ports:
                        self.access_granted = True
                        print("🔓 ACCESO OTORGADO - Secuencia completa detectada")

                    conn.close()
                except socket.timeout:
                    continue
                except OSError:
                    break
        except Exception:
            pass
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

    def _protected_service_server(self):
        """Servidor que simula el servicio protegido (ej: SSH)"""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", self.protected_service_port))
            sock.listen(5)
            sock.settimeout(0.5)
            self.protected_socket = sock

            while self.servers_running:
                try:
                    conn, addr = sock.accept()

                    # Solo aceptar conexión si se completó el knock sequence
                    if self.access_granted:
                        response = b"SSH-2.0-OpenSSH_8.9p1 - Conexion permitida\n"
                        conn.send(response)
                        print(f"✓ Conexión al servicio protegido PERMITIDA desde {addr}")
                    else:
                        print(f"✗ Conexión al servicio protegido RECHAZADA desde {addr}")

                    conn.close()
                except socket.timeout:
                    continue
                except OSError:
                    break
        except Exception:
            pass
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

    def test_full_knock_sequence_and_access(self):
        """
        Test completo: 5 knocks exitosos + conexión al servicio protegido
        """
        print("\n" + "=" * 60)
        print("TEST DE INTEGRACIÓN: SECUENCIA COMPLETA DE PORT KNOCKING")
        print("=" * 60)

        # Crear knocker apuntando a localhost
        knocker = PortKnocker()

        # Definir secuencia de 5 knocks
        knock_sequence = [(8881, "tcp"), (5555, "tcp"), (2222, "tcp"), (9999, "tcp"), (7777, "tcp")]

        print("\n[FASE 1] Ejecutando secuencia de 5 knocks...")
        knocker.execute_sequence("127.0.0.1", knock_sequence, 0.2, self.protected_service_port)

        # Esperar a que se procesen los knocks
        time.sleep(0.5)

        # Verificar que se recibieron todos los knocks
        print(f"\n[VERIFICACIÓN] Knocks recibidos: {len(self.knock_sequence_received)}/5")
        self.assertEqual(len(self.knock_sequence_received), 5)
        self.assertEqual(self.knock_sequence_received, self.knock_ports)

        # Verificar que se otorgó acceso
        print(f"[VERIFICACIÓN] Acceso otorgado: {self.access_granted}")
        self.assertTrue(self.access_granted)

        # Intentar conectar al servicio protegido
        print(
            f"\n[FASE 2] Intentando conectar al servicio protegido (puerto {self.protected_service_port})..."
        )

        service_sock = None
        try:
            service_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            service_sock.settimeout(3.0)
            service_sock.connect(("127.0.0.1", self.protected_service_port))

            # Leer respuesta del servidor
            response = service_sock.recv(1024)

            print(f"[ÉXITO] Respuesta del servidor: {response.decode().strip()}")

            # Verificar que recibimos respuesta
            self.assertIn(b"Conexion permitida", response)

        except Exception as e:
            self.fail(f"No se pudo conectar al servicio protegido: {e}")
        finally:
            if service_sock:
                service_sock.close()

        print("\n" + "=" * 60)
        print("✓ TEST COMPLETADO EXITOSAMENTE")
        print("  - 5 knocks ejecutados correctamente")
        print("  - Acceso otorgado por el firewall simulado")
        print("  - Conexión al servicio protegido establecida")
        print("=" * 60 + "\n")

    def test_incomplete_knock_sequence_denied(self):
        """
        Test: secuencia incompleta debe denegar acceso
        """
        print("\n[TEST] Secuencia incompleta (solo 3 de 5 knocks)")

        knocker = PortKnocker()

        # Solo hacer 3 knocks de 5
        incomplete_sequence = [(8881, "tcp"), (5555, "tcp"), (2222, "tcp")]

        knocker.execute_sequence("127.0.0.1", incomplete_sequence, 0.1, self.protected_service_port)
        time.sleep(0.3)

        # Verificar que NO se otorgó acceso
        self.assertFalse(self.access_granted)
        print("✓ Acceso correctamente DENEGADO con secuencia incompleta\n")

    def test_wrong_knock_order_denied(self):
        """
        Test: orden incorrecto debe denegar acceso
        """
        print("\n[TEST] Secuencia en orden incorrecto")

        knocker = PortKnocker()

        # Secuencia en orden incorrecto
        wrong_sequence = [
            (5555, "tcp"),  # Orden incorrecto
            (8881, "tcp"),
            (2222, "tcp"),
            (9999, "tcp"),
            (7777, "tcp"),
        ]

        knocker.execute_sequence("127.0.0.1", wrong_sequence, 0.1, self.protected_service_port)
        time.sleep(0.3)

        # Verificar que NO se otorgó acceso
        self.assertFalse(self.access_granted)
        print("✓ Acceso correctamente DENEGADO con orden incorrecto\n")


if __name__ == "__main__":
    unittest.main()
