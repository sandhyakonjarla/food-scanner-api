#!/bin/bash
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-osd
export TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"
