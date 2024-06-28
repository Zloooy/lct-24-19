from typing import Any, Awaitable, Callable, Coroutine, Dict, List, Union
from enum import Enum
from pydantic import BaseModel


type PromptParams = Dict[str, Any]

class GeneratorConfig(BaseModel):
    dummyApi: bool
    llmKey: str
    tavilyApiKey: str
    llmPreset: str

class ReportTopicEnum(Enum):
    CUSTOM = "CUSTOM"
    INNOVATION_NEWS = "INNOVATION_NEWS"
    COMPETITOR_REVIEW = "COMPETITOR_REVIEW"
    COMPETITORS_REVIEW = "COMPETITORS_REVIEW"
    MARKET_ANALYSIS = "MARKET_ANALYSIS"
    PRODUCT_COMPARISON = "PRODUCT_COMPARISON"

class ResearchRequest(BaseModel):
    config: GeneratorConfig
    reportTopic: ReportTopicEnum
    promptParams: PromptParams
    task: Any

class ResearchResultMetadataRequest(BaseModel):
    source_urls: List[str]

class ReResearchRequest(BaseModel):
    config: GeneratorConfig
    document: str
    medatada: ResearchResultMetadataRequest
    prompt: str
    selectionStart: int
    selectionLength: int

class ResearchResultMetadata:
    source_urls: List[str]

class ResearchResult:
    metadata: ResearchResultMetadata
    markdown: str


class PromptGeneratorResult(BaseModel):
    prompt: str
    extra_sources: Union[List[str], None] = None


type PromptGenerator = Callable[[PromptParams], PromptGeneratorResult]

type PromptExecutor = Callable[[PromptGenerator, ResearchRequest], Awaitable[ResearchResult]]

type PromptReExecutor = Callable[[ReResearchRequest], Coroutine[Any, Any, ResearchResult]]
