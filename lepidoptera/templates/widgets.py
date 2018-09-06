from markdownx.widgets import AdminMarkdownxWidget


class LepidopteraAdminMarkdownxWidget(AdminMarkdownxWidget):
    template_name = 'lepidoptera/markdownx/widget2.html'  # We don't implement the template for old Django versions (see parents classes) since this project start its life with Django 2.1