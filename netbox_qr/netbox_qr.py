import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_stream

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