from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return six.text_type(email) + six.text_type(timestamp)


verification_token_generator = TokenGenerator()
