FROM tensorflow/tensorflow:2.10.0

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY carbotrack_code /carbotrack_code
COPY api /api
COPY setup.py /setup.py
RUN pip install --upgrade pip

# We already have a make command for that!
COPY Makefile /Makefile

CMD uvicorn carbotrack.api.api:app --host 0.0.0.0 --port ${PORT:-8000}
