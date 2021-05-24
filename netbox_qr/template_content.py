"""Netbox QR Code template content."""

import base64
from io import BytesIO
from extras.plugins import PluginTemplateExtension
from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_stream
import segno

__qrcode_data_max__ = 4296


def pil2pngdatauri(img):
    """Convert Pillow image to data uri."""
    output = BytesIO()
    img.save(output, "PNG")
    data64 = base64.b64encode(output.getvalue())
    return u"data:image/png;base64," + data64.decode("utf-8")


def image_ensure_text_in_image(img, config, obj):
    """Checks if text is wanted below or next to the QR Code."""
    img_text = Image.new('L', img.size, 'white')
    text = generate_qrcode_data(config, obj, "text_fields")
    draw = ImageDraw.Draw(img_text)
    draw.text((0, 0), text, font=get_font(config,32), fill='black')
    return img_text

def get_font(config, size=32):
    file_path = resource_stream(__name__, "fonts/" + config.get("font") + ".ttf")
    font = ImageFont.truetype(file_path, size)
    return font


def image_ensure_data_in_image(img, config, obj):
    if config.get("data_in_image") and config.get("data_in_image") != None:
        if getattr(obj, config.get("data_in_image"), None):
            """Get a font."""
            file_path = resource_stream(__name__, "fonts/" + config.get("font") + ".ttf")
            font = ImageFont.truetype(file_path, 20)
            """Get a drawing context."""
            draw = ImageDraw.Draw(img)
            """Get text from the object."""
            text = getattr(obj, config.get("data_in_image"))
            """Calculate Text size and area."""
            text_width, text_height = draw.textsize(text, font=font)
            text_area = text_width * text_height
            """Calculate Image area."""
            img_area = img.width * img.height
            if text_area * 100 / img_area < 28:
                """Only draw the data in the center of the QR Code if its area is not more than 30 percent of the whole QR Code."""
                bbox = [
                    (
                        img.width / 2 - text_width / 2,
                        img.height / 2 - text_height / 2,
                    ),
                    (
                        img.width / 2 + text_width / 2,
                        img.height / 2 + text_height / 2,
                    ),
                ]
                """Box size must not be bigger than 30 percent of the whole image."""
                draw.rectangle(bbox, fill="white")
                draw.text(
                    (
                        img.width / 2 - text_width / 2,
                        img.height / 2 - text_height / 2,
                    ),
                    text,
                    font=font,
                )
    return img


def generate_qrcode_data(config, obj, fields="data_fields", url=None):
    """Generate the QRCode Data from configured data_fields."""
    data = ""
    count = 0
    if url != None:
        count += len(url)
    if config.get(fields):
        data = []
        for data_field in config.get(fields, []):
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
                            data_to_append = getattr(obj, data_field).get(cfn)
                            if count + len(data_to_append) < __qrcode_data_max__:
                                data.append("{}".format(data_to_append))
                                count += len(data_to_append)
                    except AttributeError:
                        pass
                else:
                    if data_field == "length":
                        data_to_append = str(getattr(obj, data_field)) + " " + getattr(obj, "length_unit")
                        if count + len(data_to_append) < __qrcode_data_max__:
                            data.append(
                                "{}".format(data_to_append)
                            )
                            count += len(data_to_append)
                    elif data_field in ("termination_a", "termination_b"):
                        try:
                            data_to_append = str(getattr(obj, data_field).device) + " " + str(getattr(obj, data_field))
                            if count + len(data_to_append) < __qrcode_data_max__:
                                data.append(
                                    "{}".format(data_to_append)
                                )
                                count += len(data_to_append)
                        except AttributeError:
                            pass
                    else:
                        data_to_append = getattr(obj, data_field)
                        if count + len(data_to_append) < __qrcode_data_max__:
                            data.append("{}".format(data_to_append))
                            count += len(data_to_append)
            elif data_field == "url":
                data.append("{}".format(url))
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

        """Add the URL at the end of the data field."""
        qrcodedata = generate_qrcode_data(config, obj, "data_fields", url)

        """Generate the base QR Code Image."""
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
