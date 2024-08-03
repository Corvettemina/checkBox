import asposeslidescloud
import shutil
from asposeslidescloud.apis.slides_api import SlidesApi
from asposeslidescloud.models import *
import time

from asposeslidescloud.apis.slides_async_api import SlidesAsyncApi


slides_asyncapi = SlidesAsyncApi(
            None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")

presentaionsArray = []

for count in range (0,10):
    presentation = PresentationToMerge()
    presentation.path = str(count) + ".pptx"
    presentation.source = "Storage"

    presentaionsArray.append(presentation)


# request = OrderedMergeRequest()
# request.presentations = presentaionsArray
# response = slides_api.merge_and_save_online_with_http_info(
#     "MyPresentation.pptx", None,  request, "internal", _request_timeout=5000000, is_async=False)

# request = OrderedMergeRequest()
# request.presentations = presentaionsArray
# operation_id = slides_asyncapi.start_merge_and_save(out_path="MyPresentation.pptx", files=None,  request=request, storage="internal")

# while True:
#     time.sleep(2)
#     operation = slides_asyncapi.get_operation_status(operation_id)
#     print(f"Current operation status: { operation.status }")
#     if operation.status == 'Started':
#         if operation.progress != None:
#             print(f"Operation is in progress. Merged { operation.progress.step_index } of { operation.progress.step_count }.")
#     elif operation.status == 'Canceled':
#         break
#     elif operation.status == 'Failed':
#         print(operation.error)
#         break
#     elif operation.status == 'Finished': 
#         result_path = slides_asyncapi.get_operation_result(operation_id)
#         print(f"The merged document was saved to: { result_path }")
#         break

slides_api = SlidesApi(
    None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")

slides_api.delete_unused_master_slides("MyPresentation.pptx", True)