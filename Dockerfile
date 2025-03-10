# Use an official Python runtime as a parent image
FROM python:3.10

# Install system dependencies, including Tesseract and English language files
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-osd && \
    mkdir -p /usr/share/tesseract-ocr/4.00/tessdata/ && \
    cp -r /usr/share/tesseract-ocr/4.00/tessdata/* /usr/share/tesseract-ocr/4.00/tessdata/

# Set the Tesseract language data prefix
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI runs on
EXPOSE 10000

# Command to run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
