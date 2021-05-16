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


class QRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content."""

    def x_page(self):
        """Generate Content for page."""
        config = self.context["config"]
        obj = self.context["object"]
        request = self.context["request"]
        url = request.build_absolute_uri(obj.get_absolute_url())
        # get object settings
        obj_cfg = config.get(self.model.replace("dcim.", ""))
        # Check for format request
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
            "netbox_qr/qr.html",
            extra_context={"qr": generate_qrcode(self, 2), "with_text": with_text},
        )


class DeviceQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Devices."""

    model = "dcim.device"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


class RackQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Racks."""

    model = "dcim.rack"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


class CableQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Cables."""

    model = "dcim.cable"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


class LocationQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Locations."""

    model = "dcim.location"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


class PowerPanelQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Power Panels."""

    model = "dcim.powerpanel"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


class PowerFeedQRCodeContent(QRCodeContent):
    """Generate QR Code Content for Power Feeds."""

    model = "dcim.powerfeed"

    def right_page(self):
        """Show QR Code Content on right side of view."""
        return self.x_page()


template_extensions = [
    DeviceQRCodeContent,
    RackQRCodeContent,
    CableQRCodeContent,
    LocationQRCodeContent,
    PowerPanelQRCodeContent,
    PowerFeedQRCodeContent,
]
