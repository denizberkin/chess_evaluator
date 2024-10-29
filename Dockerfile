# 3 GB as compressed image
FROM pytorch/pytorch:2.5.1-cuda11.8-cudnn9-runtime

# set workdir
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# for future implementation
CMD ["python", "main.py"]