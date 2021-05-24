"""Supporting functions to generate QR Codes for NetBox."""
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


def get_concat_h(im1, im2):
    """Concatenate two images horizontally."""
    dst = Image.new("RGB", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    """Concatenate two images vertically."""
    dst = Image.new("RGB", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]


def image_ensure_text_in_image(img, config, obj, text_below = False):
    """Generate a new empty image."""
    if text_below:
        # Generate the text variable.
        text = generate_data_from_fields(config, obj, "text_below_fields", None, 8000)
        # split text to lines every 12 characters
        text_splitted = split(text, 12)
        text = "\r\n".join(text_splitted)
        lines = len(text_splitted)
        # Generate empty Image
        img_text = Image.new("L", (img.width, lines*12), "white")
        
        # Now try the biggest possible font size.
        font_size = 56
        flag = True
        while flag:
            font = get_font(config, font_size)
            draw = ImageDraw.Draw(img_text)
            text_width, text_height = draw.textsize(text, font=font)
            if text_width < img.width and text_height < lines*12:
                flag = False
            font_size -= 1
        # Now draw the text to img_text.
        draw.text(
            (0, 0),
            text,
            font=font,
            fill="black",
        )
        # Now put the two images together.
        img_text_concat = get_concat_v(img, img_text)
    else:
        img_text = Image.new("L", (img.width * 2, img.height), "white")
        # Generate the text variable.
        text = generate_data_from_fields(config, obj, "text_fields", None, 8000)
        # Now try the biggest possible font size.
        font_size = 56
        flag = True
        while flag:
            font = get_font(config, font_size)
            draw = ImageDraw.Draw(img_text)
            text_width, text_height = draw.textsize(text, font=font)
            if text_width < img.width * 2 and text_height < img.height:
                flag = False
            font_size -= 1
        # Now draw the text to img_text.
        draw.text(
            ((img.width * 2 - text_width) / 2, (img.height - text_height) / 2),
            text,
            font=font,
            fill="black",
        )
        # Now put the two images together.
        img_text_concat = get_concat_h(img, img_text)
    return img_text_concat


def get_font(config, size=32):
    """Try to load the given font or load a "better than nothing" default font."""
    file_path = resource_stream(__name__, "fonts/" + config.get("font") + ".ttf")
    try:
        return ImageFont.truetype(file_path, size)
    except Exception:
        return ImageFont.load_default()


def image_ensure_data_in_image(img, config, obj):
    """Check if data in the center of the QR Code is wanted and generate it."""
    if config.get("data_in_image") and config.get("data_in_image") is not None:
        if getattr(obj, config.get("data_in_image"), None):
            # Get a font.
            file_path = resource_stream(
                __name__, "fonts/" + config.get("font") + ".ttf"
            )
            font = ImageFont.truetype(file_path, 20)
            # Get a drawing context.
            draw = ImageDraw.Draw(img)
            # Get text from the object.
            text = getattr(obj, config.get("data_in_image"))
            # Calculate Text size and area.
            text_width, text_height = draw.textsize(text, font=font)
            text_area = text_width * text_height
            # Calculate Image area.
            img_area = img.width * img.height
            if text_area * 100 / img_area < 28:
                # Only draw the data in the center of the QR Code if its area
                # is not more than 28 percent of the whole QR Code.
                # Should be 30 percent, but this is not working.
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
                # Box size must not be bigger than 30 percent of the whole image.
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


def generate_data_from_fields(
    config, obj, fields="data_fields", url=None, __data_max_length__=4296
):
    """Generate the QRCode Data from configured data_fields."""
    data = ""
    count = 0
    if url is not None:
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
                            if count + len(data_to_append) < __data_max_length__:
                                data.append("{}".format(data_to_append))
                                count += len(data_to_append)
                    except AttributeError:
                        pass
                else:
                    if data_field == "length":
                        data_to_append = (
                            str(getattr(obj, data_field))
                            + " "
                            + getattr(obj, "length_unit")
                        )
                        if count + len(data_to_append) < __data_max_length__:
                            data.append("{}".format(data_to_append))
                            count += len(data_to_append)
                    elif data_field in ("termination_a", "termination_b"):
                        try:
                            data_to_append = (
                                str(getattr(obj, data_field).device)
                                + " "
                                + str(getattr(obj, data_field))
                            )
                            if count + len(data_to_append) < __data_max_length__:
                                data.append("{}".format(data_to_append))
                                count += len(data_to_append)
                        except AttributeError:
                            pass
                    else:
                        data_to_append = getattr(obj, data_field)
                        if count + len(data_to_append) < __data_max_length__:
                            data.append("{}".format(data_to_append))
                            count += len(data_to_append)
            elif data_field == "url":
                data.append("{}".format(url))
        data = "\r\n".join(data)
    return data
