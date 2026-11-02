
FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

COPY . .

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "active-fault-explorer", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
