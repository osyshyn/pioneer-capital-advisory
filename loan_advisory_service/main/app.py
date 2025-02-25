from dishka.integrations.fastapi import setup_dishka, AsyncContainer
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from loan_advisory_service.main.di import setup_di






def get_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    di_container = setup_di()
    setup_dishka(di_container, app)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "loan_advisory_service.main.app:get_app",
        host="0.0.0.0",
        port=8000,
        factory=True,
        reload=True,
        forwarded_allow_ips="*",
        proxy_headers=True,
    )
