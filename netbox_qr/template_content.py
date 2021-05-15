from extras.plugins import PluginTemplateExtension
import segno

class DeviceContent(PluginTemplateExtension):
    model = 'dcim.cable'

    def right_page(self):
        test = "Test"
        qr = segno.make('Yellow Submarine')
        return self.render('netbox_qr/device_qr.html', extra_context={
            'image': qr,
        })

template_extensions = [DeviceContent]
