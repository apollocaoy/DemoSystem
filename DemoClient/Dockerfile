FROM python
COPY worker.py worker.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "worker.py"]