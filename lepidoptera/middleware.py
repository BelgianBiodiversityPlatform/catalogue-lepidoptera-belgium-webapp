from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class LepidopteraLocaleMiddleware(LocaleMiddleware):
    # We need to customize things, because:
    #   - LANGUAGES should include FR, EN, NL, DE because it is used by things such as ModelTranslations (to be
    #     confirmed 100%)
    #   - But not all those languages are supported in the website (for example, page fragments are missing)
    #   - And sometimes, users may end up with one of those "currently unsupported" languages selected (that happened to
    #     me in development, probably because French was previously selected and still stored in my session...) I guess
    #     that could also happen because of browser preferences?
    #
    #  So, just to be safe, we define our own LocaleMiddleware, who in addition to the standard one, redirect to the
    #  default language (SETTINGS.language_code), in case the requested language is not listed in our
    #  settings.LANGUAGES_AVAILABLE_IN_SELECTOR
    def process_request(self, request):
        super().process_request(request)

        if request.LANGUAGE_CODE not in [lang[0] for lang in settings.LANGUAGES_AVAILABLE_IN_SELECTOR]:
            language = settings.LANGUAGE_CODE
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()