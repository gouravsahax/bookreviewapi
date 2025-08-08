# use python 3.11 base img
FROM python:3.11-slim

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first to leverage Docker cache
COPY requirements.txt .

# install python dependencies (include python-dotenv)
RUN pip install --no-cache-dir -r requirements.txt

# copy everything else, including .env file
COPY . .

# expose FastAPI port
EXPOSE 8000

# run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]