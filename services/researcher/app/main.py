import asyncio
import os

import prompt_generators.market_analysis
import prompt_generators.product_compare

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) "
    + "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
)

from fastapi import FastAPI, HTTPException

from dto import PromptExecutor, PromptGenerator, PromptReExecutor, ReResearchRequest, ResearchRequest, ReportTopicEnum, PromptGeneratorResult

import prompt_re_executors.dummy
import prompt_re_executors.gptr

import prompt_executors.dummy
import prompt_executors.gptr

import prompt_generators.innovation_news
import prompt_generators.competitor_review
import prompt_generators.competitors_review
import prompt_generators.custom


app = FastAPI(
    title="Report generation service",
    description="Api for generating a report on a specific topic"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/research", operation_id="research", description="Initially generate report", response_model=PromptGeneratorResult)
def research(request: ResearchRequest):
    # Choose prompt executor
    executor: PromptExecutor
    if request.config.dummyApi:
        executor = prompt_executors.dummy.execute_prompt
    else:
        executor = prompt_executors.gptr.execute_prompt
        # raise HTTPException(status_code=400, detail="Can not choose prompt executor")

    report_topic_generator_map: dict[ReportTopicEnum, PromptGenerator] = {
        ReportTopicEnum.CUSTOM: prompt_generators.custom.generate_prompt,
        ReportTopicEnum.INNOVATION_NEWS: prompt_generators.innovation_news.generate_prompt,
        ReportTopicEnum.COMPETITOR_REVIEW: prompt_generators.competitor_review.generate_prompt,
        ReportTopicEnum.COMPETITORS_REVIEW: prompt_generators.competitors_review.generate_prompt,
        ReportTopicEnum.MARKET_ANALYSIS: prompt_generators.market_analysis.generate_prompt,
        ReportTopicEnum.PRODUCT_COMPARISON: prompt_generators.product_compare.generate_prompt
    }
    if request.reportTopic not in report_topic_generator_map:
        raise HTTPException(status_code=400, detail="Can not choose prompt generator")
    # Execute prompt
    return asyncio.run(executor(report_topic_generator_map[request.reportTopic], request))


@app.post("/re-research", operation_id="reResearch", description="Generate modified report based on one taken from /research", response_model=PromptGeneratorResult)
def re_research(request: ReResearchRequest):
    # Choose executor
    executor: PromptReExecutor
    if request.config.dummyApi:
        executor = prompt_re_executors.dummy.re_execute_prompt
    else:
        executor = prompt_re_executors.gptr.re_execute_prompt

    # Execute
    return asyncio.run(executor(request))
