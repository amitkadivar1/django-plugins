from django.db import models
import imp
import os

class Plugin(models.Model):
    plugin_file = models.FileField(upload_to='plugins/')
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255, editable=False)
    author = models.CharField(max_length=255, editable=False)
    acts_on = models.CharField(max_length=255, editable=False)
    
    #if use python 2 then use unicode 
    # def __unicode__(self):
    #     return self.title
    #if use python 3 then use str like this
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Plugin, self).save(*args, **kwargs)
        plg = self.get_class()
        if hasattr(plg, 'Meta'):
            self.title = plg.Meta.name
            self.author = plg.Meta.author
            self.acts_on = plg.Meta.acts_on
        else:
            self.title = ''
            self.author = ''
            self.acts_on = ''
        super(Plugin, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        extra_file = '%sc' % self.get_plugin_file_filename()
        try:
            os.remove(extra_file)
        except OSError:
            pass
        super(Plugin, self).delete(*args, **kwargs)
    
    def get_class(self):
        path, filename = os.path.split(self.get_plugin_file_filename())
        filename, ext = os.path.splitext(filename)
        fp, pathname, description = imp.find_module(filename, [path])
        module = imp.load_module(filename, fp, pathname, description)
        return module.plugin_class
        
    class Admin:
        fields = (
            (None, {
                'fields': ('plugin_file',)
            }),
            (None, {
                'fields': ('active',)
            }),
        )
        list_display = ('title', 'author', 'acts_on', 'active')
        list_filter = ('active', 'acts_on')
        search_fields=('title','author')
