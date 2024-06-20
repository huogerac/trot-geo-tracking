from ninja import NinjaAPI
from ninja.errors import ValidationError
from django.http import JsonResponse

from ..base.views import router as base_router

# from ..accounts.views import router as accounts_router
from ..core.views import router as core_router
from ..base.exceptions import ServiceUnavailableError, BusinessError

api = NinjaAPI(
    csrf=True,
    title="🥷 geotracking",
    description="Geo Tracking",
)

api.add_router("/", base_router, tags=["base"])
# api.add_router("/accounts/", accounts_router, tags=["accounts"])
api.add_router("/core/", core_router, tags=["core"])


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    def parse_input_validation(error):
        field_path = [f for f in error.get("loc") if type(f) is str]
        field = ".".join(field_path)
        return f"{field}: {error.get('msg')} ({error.get('type')})"

    error = ""
    if len(exc.errors) >= 1:
        error = parse_input_validation(exc.errors[0])
    return JsonResponse({"message": f"[INVALID INPUT] {error}"}, status=422)


@api.exception_handler(ServiceUnavailableError)
def service_unavailable_errors(request, exc):
    error = str(exc)
    return JsonResponse(
        {
            "message": f"[UNAVAILABLE] Me desculpe! Serviço não disponível no momento. Tente mais tarde: {error}"
        },
        status=503,
    )


@api.exception_handler(BusinessError)
def business_errors(request, exc):
    error = str(exc)
    return JsonResponse({"message": f"[ERROR] {error}"}, status=400)
