import logging

from django.shortcuts import render
from web.auth.decorators import require_registered
from web.domains.case.access.models import AccessRequestProcess

logger = logging.getLogger(__name__)


@require_registered
def workbasket(request):
    logger.debug(f"{request.user} workbasket")
    process = AccessRequestProcess.objects.owned_process(request.user)
    return render(request, 'web/workbasket.html', {'process_list': process})
