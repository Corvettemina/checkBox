from asposeslidescloud.apis.slides_api import SlidesApi
from asposeslidescloud.models import *


slides_api = SlidesApi(
    None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")

slides_api.delete_unused_master_slides("MyPresentation.pptx", True)