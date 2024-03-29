FROM bitnami/pytorch

# Set environment variable
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache

# Set working directory
WORKDIR /app

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY raw_data raw_data
COPY carbotrack_code carbotrack_code
COPY api api
COPY setup.py /setup.py
RUN pip install --upgrade pip

# We already have a make command for that!
COPY Makefile /Makefile

CMD uvicorn api.api:app --host 0.0.0.0 --port ${PORT:-7777}
