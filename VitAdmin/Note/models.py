from django.db import models

# Create your models here.
class Note(models.Model):
    nt_id = models.CharField(max_length = 20, primary_key=True, editable=False)
    nt_title = models.CharField(max_length=200)
    nt_subtitle = models.CharField(max_length=200, blank=True, null=True)
    nt_content = models.TextField()
    nt_img = models.ImageField(max_length=255, blank=True, null=True)
    nt_pdf = models.FileField(max_length=255, blank=True, null=True)
    nt_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.nt_id:
            last_note = Note.objects.order_by('-nt_id').first()
            if last_note:
                last_id = int(last_note.nt_id.replace('NT', ''))
                new_id = 'NT' + str(last_id + 1).zfill(3)
            else:
                new_id = 'NT001'
            self.nt_id = new_id
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
