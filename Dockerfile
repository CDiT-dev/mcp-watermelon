FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/watermelon_mcp/ src/watermelon_mcp/

RUN pip install --no-cache-dir .

ENV MCP_TRANSPORT=streamable-http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/mcp', timeout=5)" || exit 1

CMD ["server"]
