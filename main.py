from fastapi import FastAPI
import logging
import uvicorn

logging.basicConfig(format='%(levelname)s - %(asctime)s:\n\t%(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

app = FastAPI()


@app.get("/doCall")
def doCall(userId: int, msg: str):
    logging.debug("Se manda el mensaje '%s' al usuario %i", msg, userId)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
