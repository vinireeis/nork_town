# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

WORKDIR /nork_town

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# PORT
EXPOSE 5000

COPY . .

# ENVS
ENV HOST_URL="sqlite:///server.db"
ENV CAR_LIMIT=2

CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0:5000"]
