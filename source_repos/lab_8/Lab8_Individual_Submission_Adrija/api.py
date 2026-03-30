from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request

from ai_app.agent import DisasterForecastAgent
from ai_app.config import BASE_DIR
from ai_app.evaluation import run_sample_evaluation
from ai_app.logging_utils import configure_logging
from ai_app.models import HealthResponse, QueryRequest, QueryResponse
from ai_app.monitoring import MonitoringService


app = FastAPI(title="Disaster Forecast AI Application")
agent = DisasterForecastAgent()
monitoring_service = MonitoringService()
logger = configure_logging(BASE_DIR)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    start = perf_counter()
    logger.info("request_started id=%s path=%s method=%s", request_id, request.url.path, request.method)
    try:
        response = await call_next(request)
        latency_ms = (perf_counter() - start) * 1000
        logger.info(
            "request_completed id=%s path=%s status=%s latency_ms=%.2f",
            request_id,
            request.url.path,
            response.status_code,
            latency_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as exc:
        latency_ms = (perf_counter() - start) * 1000
        monitoring_service.record_error(request.url.path, latency_ms, str(exc))
        logger.exception(
            "request_failed id=%s path=%s latency_ms=%.2f error=%s",
            request_id,
            request.url.path,
            latency_ms,
            exc,
        )
        raise


@app.get("/health", response_model=HealthResponse)
def health_check():
    return agent.health()


@app.post("/generate", response_model=QueryResponse)
def generate_explanation(request: QueryRequest):
    started = perf_counter()
    result = agent.answer(
        instruction=request.instruction,
        user_input=request.input,
        region=request.region,
        top_k=request.top_k,
    )
    latency_ms = (perf_counter() - started) * 1000
    monitoring_service.record_success(
        path="/generate",
        latency_ms=latency_ms,
        used_fallback_model=result["used_fallback_model"],
    )
    logger.info(
        "generation_completed region=%s top_k=%s fallback=%s latency_ms=%.2f",
        request.region,
        request.top_k,
        result["used_fallback_model"],
        latency_ms,
    )
    return QueryResponse(**result)


@app.get("/architecture")
def architecture():
    return {
        "layers": [
            "Data Sources",
            "Knowledge Base",
            "Retrieval Pipeline",
            "Domain-Adapted Model",
            "AI Agent Reasoning",
            "Snowflake Data Warehouse",
            "Application Interface",
            "Monitoring and Deployment",
        ]
    }


@app.get("/metrics")
def metrics():
    return monitoring_service.summary()


@app.get("/evaluation")
def evaluation():
    report = run_sample_evaluation(agent)
    logger.info("evaluation_completed scenarios=%s", report["scenario_count"])
    return report


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
