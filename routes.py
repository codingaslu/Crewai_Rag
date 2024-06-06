from fastapi import APIRouter
# from friendly_healthcare_expert import chat_response as friendly_response
from crypto_expert import chat_response as authoritative_response
# from learn_from_me import chat_response as learn_response
# from upload import upload_file
router = APIRouter()

# router.post("/upload_file/")(upload_file)
# router.post("/chat_response_frdqa")(friendly_response)
router.post("/chat_response_qa")(authoritative_response)
# router.post("/chat_response_learn")(learn_response)


# router.post("/chat_response_learn")(chat_response.chat_response_learn)
# router.post("/chat_response_qa")(chat_response.chat_response_qa)
# router.post("/upload_file/")(upload_file.upload_file)