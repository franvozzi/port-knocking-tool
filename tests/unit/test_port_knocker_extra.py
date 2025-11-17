import time
from src.core.port_knocker import PortKnocker


def test_execute_sequence_success(monkeypatch):
    pk = PortKnocker(verbose=False)

    # Evitar duerme para acelerar tests
    monkeypatch.setattr(time, "sleep", lambda s: None)

    # Estado inicial: puerto cerrado
    monkeypatch.setattr(pk, "_tcp_ping", lambda ip, port, timeout=1: False)

    # Knock siempre exitoso
    monkeypatch.setattr(pk, "_knock_port", lambda ip, port, protocol: True)

    # Verificación final indica puerto abierto
    monkeypatch.setattr(
        pk,
        "_verify_port_open",
        lambda ip, port: {
            "open": True,
            "success_count": 1,
            "total_attempts": 3,
            "avg_latency": 12.3,
        },
    )

    result = pk.execute_sequence("127.0.0.1", [(7000, "tcp"), (8000, "tcp")], 0.01, 1194)
    assert result is True


def test_execute_sequence_failure(monkeypatch):
    pk = PortKnocker(verbose=False)

    # Evitar duerme para acelerar tests
    monkeypatch.setattr(time, "sleep", lambda s: None)

    # Estado inicial: puerto cerrado
    monkeypatch.setattr(pk, "_tcp_ping", lambda ip, port, timeout=1: False)

    # Knock siempre exitoso
    monkeypatch.setattr(pk, "_knock_port", lambda ip, port, protocol: True)

    # Verificación final indica puerto cerrado
    monkeypatch.setattr(
        pk,
        "_verify_port_open",
        lambda ip, port: {"open": False, "success_count": 0, "total_attempts": 3, "avg_latency": 0},
    )

    result = pk.execute_sequence("127.0.0.1", [(7000, "tcp")], 0.01, 1194)
    assert result is False
