FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash app_user
RUN chown $USER:$USER -R /home/app_user
RUN chmod 777 /home/app_user
WORKDIR /home/app_user
ADD battleship_runner.py .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER $USER
COPY . .
CMD ["python","battleship_runner.py", "-p1_name", "suman" ,"-p1", "player1_board.json", "-p2_name", "neha", "-p2", "player2_board.json"]