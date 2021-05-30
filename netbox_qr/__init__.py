"""Plugin declaration."""

from extras.plugins import PluginConfig


class QRConfig(PluginConfig):
    """Plugin configuration for the netbox_qr plugin."""

    name = "netbox_qr"
    verbose_name = "QR Code plugin for netbox."
    version = "0.1.1"
    author = "Florian Meyer"
    description = "A netbox plugin for generating qr codes for specific pages."
    base_url = "qr"
    required_settings = []
    default_settings = {
        "with_text": True,
        "font": "Roboto-Regular",
        "data_fields": ["name", "serial", "url"],
        "text_fields": ["name", "serial"],
        "text_below_fields": ["name"],
        "cable": {
            "data_fields": [
                "label",
                "termination_a",
                "termination_b",
                "type",
                "length",
                "url",
            ],
            "data_in_image": "label",
            "text_fields": ["label"],
            "text_below_fields": ["label"],
        },
    }
    caching_config = {}


config = QRConfig  # pylint:disable=invalid-name
