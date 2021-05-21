"""Netbox QR Code template content."""

import base64
from io import BytesIO
from extras.plugins import PluginTemplateExtension
from PIL import ImageDraw, ImageFont
import segno


def generate_qrcode_image(self, scale=10, qrcodedata="", error="l"):
    """Generate QR Code."""
    # qrcode = segno.make_qr(qrcodedata, error="H").png_data_uri(scale=scale)
    qrcode = segno.make(qrcodedata, error="H")
    return qrcode


def pil2pngdatauri(img):
    """Convert Pillow image to data uri."""
    output = BytesIO()
    img.save(output, "PNG")
    data64 = base64.b64encode(output.getvalue())
    return u"data:image/png;base64," + data64.decode("utf-8")


def generate_qrcode_data(config, obj):
    """Generate the QRCode Data from configured data_fields."""
    data = ""
    if config.get("data_fields"):
        data = []
        for data_field in config.get("data_fields", []):
            cfn = None
            if "." in data_field:
                try:
                    data_field, cfn = data_field.split(".")
                except ValueError:
                    cfn = None
            if getattr(obj, data_field, None):
                if cfn:
                    try:
                        if getattr(obj, data_field).get(cfn):
                            data.append("{}".format(getattr(obj, data_field).get(cfn)))
                    except AttributeError:
                        pass
                else:
                    if data_field == "length":
                        data.append(
                            "{}".format(
                                str(getattr(obj, data_field))
                                + " "
                                + getattr(obj, "length_unit")
                            )
                        )
                    elif data_field in ("termination_a", "termination_b"):
                        data.append(
                            "{}".format(
                                str(getattr(obj, data_field).device)
                                + " "
                                + str(getattr(obj, data_field))
                            )
                        )
                    else:
                        data.append("{}".format(getattr(obj, data_field)))
        data = "\r\n".join(data)
    return data


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

        """Load QRCode specific config."""
        segno_args = {}
        for k, v in config.items():
            if k.startswith("segno_"):
                segno_args[k.replace("segno_", "")] = v

        """Add the URL at the end of the data field."""
        qrcodedata = generate_qrcode_data(config, obj) + "\r\n" + url

        """Generate the base QR Code Image."""
        qrcode_image = generate_qrcode_image(self, 3, qrcodedata).to_pil(scale=3)

        """Check if we want data in the center of the QRCode."""
        if config.get("data_in_image") and config.get("data_in_image") != None:
            if getattr(obj, config.get("data_in_image"), None):
                """Get a font."""
                font = ImageFont.load_default()
                """Get a drawing context."""
                draw = ImageDraw.Draw(qrcode_image)
                """Get text from the object."""
                text = getattr(obj, config.get("data_in_image"))
                """Calculate Text size and area."""
                text_width, text_height = draw.textsize(text, font=font)
                text_area = text_width * text_height
                """Calculate Image area."""
                qrcode_image_area = qrcode_image.width * qrcode_image.height
                if text_area * 100 / qrcode_image_area <= 30:
                    """Only draw the data in the center of the QR Code if its area is not more than 30 percent of the whole QR Code."""
                    bbox = [
                        (
                            qrcode_image.width / 2 - text_width / 2 - 10,
                            qrcode_image.height / 2 - text_height / 2 - 10,
                        ),
                        (
                            qrcode_image.width / 2 + text_width / 2 + 10,
                            qrcode_image.height / 2 + text_height / 2 + 10,
                        ),
                    ]
                    """Box size must not be bigger than 30 percent of the whole image."""
                    draw.rectangle(bbox, fill="blue")
                    draw.text(
                        (
                            qrcode_image.width / 2 - text_width / 2,
                            qrcode_image.height / 2 - text_height / 2,
                        ),
                        text,
                    )

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
