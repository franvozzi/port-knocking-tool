import logging
from pathlib import Path

from src.monitoring.logger import StructuredLogger


def count_handlers_of_type(logger, handler_type):
    return sum(1 for h in logger.handlers if isinstance(h, handler_type))


def test_multiple_instances_do_not_duplicate_handlers(tmp_path):
    # Crear dos instancias sin reiniciar el proceso
    l1 = StructuredLogger(log_file=str(tmp_path / "a.log"))
    l2 = StructuredLogger(log_file=str(tmp_path / "a.log"))

    logger = logging.getLogger("VPNConnect")

    # Debe haber exactamente 1 FileHandler y 1 StreamHandler
    assert count_handlers_of_type(logger, logging.FileHandler) == 1
    assert count_handlers_of_type(logger, logging.StreamHandler) == 1


def test_replace_filehandler_when_different_file(tmp_path):
    p1 = tmp_path / "a.log"
    p2 = tmp_path / "b.log"

    # Primera instancia crea handler apuntando a a.log
    l1 = StructuredLogger(log_file=str(p1))
    logger = logging.getLogger("VPNConnect")

    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1
    fh = file_handlers[0]
    assert Path(fh.baseFilename).resolve() == p1.resolve()

    # Segunda instancia con archivo distinto debe reemplazar el FileHandler
    l2 = StructuredLogger(log_file=str(p2))
    logger = logging.getLogger("VPNConnect")
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1
    fh2 = file_handlers[0]
    assert Path(fh2.baseFilename).resolve() == p2.resolve()
