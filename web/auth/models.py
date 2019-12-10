import logging

from django.contrib.auth.backends import ModelBackend

from web.models import User

logger = logging.getLogger(__name__)


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        authenticated_user = super().authenticate(request, username, password)

        logger.debug(authenticated_user)

        if authenticated_user is None:
            logger.info(f"there is no authenticated user for {username}")
            unauthenticated_user = User.objects.get_by_natural_key(username)

            if unauthenticated_user is not None and \
                    unauthenticated_user.account_status != User.SUSPENDED:
                unauthenticated_user.unsuccessful_login_attempts += 1
                if unauthenticated_user.unsuccessful_login_attempts > 4:
                    unauthenticated_user.account_status = User.SUSPENDED
                unauthenticated_user.save()
            else:
                logger.error(f"no unauthenticated user match for {username} this will cause a runtime error!")
        else:
            authenticated_user.unsuccessful_login_attempts = 0
            authenticated_user.save()
            return authenticated_user
