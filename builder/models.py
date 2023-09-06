from django.db import models


class Pages(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    html = models.TextField()
    css = models.TextField()
    # js = models.TextField() ???
    preview_link = models.TextField()

# TODO: Save grapeJS in djnago...
# https://chat.openai.com/share/33722e75-cc0e-4c68-a465-d73f111bb550


# --- GrapeJS Blocks HTML ---
# https://chat.openai.com/share/496e5ff5-34c3-4475-96e9-843ff3286e86

from django.db import models

class MediaObject(models.Model):
    url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.url

class BlockCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class GrapesJSBlock(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(max_length=255)
    attributes = models.JSONField()
    content = models.TextField()
    category = models.ForeignKey(BlockCategory, on_delete=models.CASCADE)
    media = models.ForeignKey(MediaObject, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.label
