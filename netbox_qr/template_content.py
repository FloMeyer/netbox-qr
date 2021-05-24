"""Netbox QR Code template content."""
from extras.plugins import PluginTemplateExtension
import segno
from .netbox_qr import generate_data_from_fields, pil2pngdatauri, image_ensure_text_in_image, image_ensure_data_in_image


class QRCodeContent(PluginTemplateExtension):
    """Generate QR Code Content."""

    def x_page(self):
        """Generate Content for page."""
        config = self.context["config"]
        obj = self.context["object"]
        request = self.context["request"]
        url = self.context["request"].build_absolute_uri(obj.get_absolute_url())

        """Get object specific settings."""
        obj_cfg = config.get(self.model.replace("dcim.", ""))
        if obj_cfg is None:
            return ""

        """Override default config."""
        config.update(obj_cfg)

        """Generate the data which is read by the qr code reader."""
        qrcodedata = generate_data_from_fields(config, obj, "data_fields", url)

        """Generate the base QR Code Image. Scale 2 because 1 would be too small."""
        qrcode_image = segno.make(qrcodedata, error="H").to_pil(scale=2, border=0)

        """Check if we want data in the center of the QRCode."""
        qrcode_image = image_ensure_data_in_image(qrcode_image, config, obj)

        """Check if we want text below or next to the QRCode."""
        qrcode_image = image_ensure_text_in_image(qrcode_image, config,obj)

        """Check for format in request, to display the right activated button on the web page."""
        if (
            "format" in self.context["request"].GET
            and self.context["request"].GET["format"] != "without_text"
        ):
            btn_with_text = True
        else:
            btn_with_text = False

        """Render the page content."""
        return self.render(
            "netbox_qr/qr.html",
            extra_context={
                "qr": pil2pngdatauri(qrcode_image),
                "with_text": btn_with_text,
            },
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
