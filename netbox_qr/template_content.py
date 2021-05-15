from extras.plugins import PluginTemplateExtension

class DeviceContent(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        test = "Test"
        return self.render('netbox_qr/device_qr.html', extra_context={
            'image': test,
        })

template_extensions = [DeviceContent]
