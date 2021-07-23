from pathlib import Path

from starlette.responses import HTMLResponse


async def homepage(request):
    with open(str(Path(__file__).parent.parent.parent / "static" / "index.html")) as f:
        idx = f.readlines()
        return HTMLResponse(
            idx[0]
        )
