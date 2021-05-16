"""Netbox QR Code template content."""

from extras.plugins import PluginTemplateExtension
import segno

# import io


def generate_qrcode(self, scale=10):
    """Generate QR Code."""
    url = self.context["request"].build_absolute_uri(
        self.context["object"].get_absolute_url()
    )
    qrcode = segno.make_qr(url).svg_data_uri(scale=scale)
    return qrcode


class DeviceQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Devices."""

    model = "dcim.device"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        # Check for export rendering (except for table-based)
        if (
            "format" in self.context["request"].GET
            and self.context["request"].GET["format"] != "without_text"
        ):
            text = self.context["request"].GET["format"]
            with_text = True
        else:
            text = None
            with_text = False
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
                "with_text": with_text
            },
        )


class RackQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Racks."""

    model = "dcim.rack"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
            },
        )


class CableQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Cables."""

    model = "dcim.cable"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
            },
        )


class LocationQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Locations."""

    model = "dcim.location"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
            },
        )


class PowerPanelQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Power Panels."""

    model = "dcim.powerpanel"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
            },
        )


class PowerFeedQRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content for Power Feeds."""

    model = "dcim.powerfeed"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.render(
            "netbox_qr/device_qr.html",
            extra_context={
                "qr": generate_qrcode(self, 2),
            },
        )


template_extensions = [
    DeviceQRCodeContent,
    RackQRCodeContent,
    CableQRCodeContent,
    LocationQRCodeContent,
    PowerPanelQRCodeContent,
    PowerFeedQRCodeContent,
]
