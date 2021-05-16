from extras.plugins import PluginTemplateExtension
import segno
#import io

class DeviceContent(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
#        qr = segno.make('Yellow Submarine')
#        buffer = io.BytesIO()
#        qr.save(buffer, format="PNG")
#        qr_b64 = "data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode("utf-8")
# working
#        qr = segno.make('Up Jumped the Devil').svg_data_uri()
        url = self.context['request'].build_absolute_uri(self.context['object'].get_absolute_url())
        qr = segno.make_qr(url).svg_data_uri(scale=10)

        return self.render('netbox_qr/device_qr.html', extra_context={
            'qr': qr,
        })

template_extensions = [DeviceContent]
