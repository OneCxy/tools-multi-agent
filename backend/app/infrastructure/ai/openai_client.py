from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from config.settings import settings


SF_API_KEY = settings.SF_API_KEY
SF_BASE_URL = settings.SF_BASE_URL
MAIN_MODEL_NAME = settings.MAIN_MODEL_NAME


AL_BAILIAN_API_KEY = settings.AL_BAILIAN_API_KEY
AL_BAILIAN_BASE_URL = settings.AL_BAILIAN_BASE_URL
SUB_MODEL_NAME = settings.SUB_MODEL_NAME



main_model_client = AsyncOpenAI(
    base_url=SF_BASE_URL, 
    api_key=SF_API_KEY  
)

sub_model_client = AsyncOpenAI(
    base_url=AL_BAILIAN_BASE_URL, 
    api_key=AL_BAILIAN_API_KEY 
)





main_model = OpenAIChatCompletionsModel(
    model=MAIN_MODEL_NAME,
    openai_client=main_model_client)


sub_model = OpenAIChatCompletionsModel(
    model=SUB_MODEL_NAME,
    openai_client=sub_model_client)
