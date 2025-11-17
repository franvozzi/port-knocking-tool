from src.utils.validators import ConfigValidator

class TestConfigValidator:
    """Tests para ConfigValidator"""
    
    def test_valid_config(self):
        """Test con configuración válida"""
        validator = ConfigValidator()
        config = {
            "target_ip": "192.168.1.1",
            "knock_sequence": [[7000, "tcp"], [8000, "tcp"]],
            "interval": 0.5,
            "target_port": 1194
        }
        assert validator.validate(config) is True
        assert len(validator.errors) == 0
    
    def test_invalid_ip(self):
        """Test con IP inválida"""
        validator = ConfigValidator()
        config = {
            "target_ip": "999.999.999.999",
            "knock_sequence": [[7000, "tcp"]],
            "interval": 0.5,
            "target_port": 1194
        }
        assert validator.validate(config) is False
        assert any("IP inválida" in error for error in validator.errors)
    
    def test_invalid_port(self):
        """Test con puerto inválido"""
        validator = ConfigValidator()
        config = {
            "target_ip": "192.168.1.1",
            "knock_sequence": [[70000, "tcp"]],  # Puerto > 65535
            "interval": 0.5,
            "target_port": 1194
        }
        assert validator.validate(config) is False
    
    def test_invalid_protocol(self):
        """Test con protocolo inválido"""
        validator = ConfigValidator()
        config = {
            "target_ip": "192.168.1.1",
            "knock_sequence": [[7000, "http"]],  # Protocolo inválido
            "interval": 0.5,
            "target_port": 1194
        }
        assert validator.validate(config) is False
    
    def test_missing_required_fields(self):
        """Test con campos requeridos faltantes"""
        validator = ConfigValidator()
        config = {"target_ip": "192.168.1.1"}
        assert validator.validate(config) is False
        assert len(validator.errors) > 0
    
    def test_validate_ip_method(self):
        """Test método validate_ip"""
        assert ConfigValidator.validate_ip("192.168.1.1") is True
        assert ConfigValidator.validate_ip("8.8.8.8") is True
        assert ConfigValidator.validate_ip("invalid") is False
        assert ConfigValidator.validate_ip("999.999.999.999") is False
    
    def test_validate_port_method(self):
        """Test método validate_port"""
        assert ConfigValidator.validate_port(80) is True
        assert ConfigValidator.validate_port(65535) is True
        assert ConfigValidator.validate_port(0) is False
        assert ConfigValidator.validate_port(70000) is False
        assert ConfigValidator.validate_port("80") is True
        assert ConfigValidator.validate_port("invalid") is False
