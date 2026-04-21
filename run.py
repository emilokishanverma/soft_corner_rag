import uvicorn

try:
    if __name__ == "__main__":
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
except Exception as e:
    raise RuntimeError(f"Failed to start server: {str(e)}")