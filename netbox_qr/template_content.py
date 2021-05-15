from extras.plugins import PluginTemplateExtension
#from .models import Animal

class DeviceContent(PluginTemplateExtension):
    model = 'dcim.content'
    img = ''
    def right_page(self):
        return self.render('netbox_qr/device_qr.html', extra_context={
            'image': img,
        })

template_extensions = [DeviceContent]
