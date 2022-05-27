FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash app_user
RUN chown -R app_user /home/app_user
RUN chmod -R 777 /home/app_user
WORKDIR /home/app_user
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER app_user
COPY . .
CMD ["bash"]