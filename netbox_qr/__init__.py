"""Plugin declaration."""

from extras.plugins import PluginConfig


class QRConfig(PluginConfig):
    """Plugin configuration for the netbox_qr plugin."""

    name = "netbox_qr"
    verbose_name = "QR Code plugin for netbox."
    version = "0.1.0"
    author = "Florian Meyer"
    description = "A netbox plugin for generating qr codes for specific pages."
    base_url = "qr"
    required_settings = []
    default_settings = {"pages": ["device", "rack", "cable"]}
    caching_config = {}


config = QRConfig  # pylint:disable=invalid-name
