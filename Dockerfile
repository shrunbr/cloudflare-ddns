# Set image
FROM python:3.13-alpine
# Set working directory
WORKDIR /code
# Copy requirements.txt from app root folder to container
COPY requirements.txt .
# Install requirements
RUN pip install -r requirements.txt
# Copy files to /code
COPY scripts/cf-ddns.py .
# Label Source
LABEL org.opencontainers.image.source=https://github.com/shrunbr/cloudflare-ddns
# Execute script
CMD ["python", "-u", "cf-ddns.py"]