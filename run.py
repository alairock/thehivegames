import os

import uvicorn

if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=3232, log_level=os.getenv('LOGLEVEL', 'info'), reload=True)
