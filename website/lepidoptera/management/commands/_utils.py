from django.core.management import BaseCommand


class LepidopteraCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(LepidopteraCommand, self).__init__(*args, **kwargs)

        self.w = self.stdout.write  # Alias to save keystrokes :)


# Used to clean text fields from Access
def text_clean(text):
    if text is not None:
        return text.strip()

    return ''
