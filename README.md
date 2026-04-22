Потоковая сегментация надводных объектов

Интеллектуальная инфраструктура для сбора и обработки морских данных в реальном времени.

### Технологический стек:
* **ML:** PyTorch (DeepLabV3+).
* **Big Data:** Apache Kafka, Apache Spark Structured Streaming.
* **Database:** PostgreSQL.
* **Interface:** Streamlit (UI), Flask (Video Streamer).
* **Infrastructure:** Docker Compose.

### Как запустить:
1. Клонировать репозиторий.
2. Запустить контейнеры: `docker-compose up -d`.
3. Запустить продюсер данных: `producer.ipynb` через ноутбук по адресу http://localhost:8888/lab/workspaces/.
4. Запусттиь спарк 'spark.ipynb' через ноутбук по адресу http://localhost:8888/lab/workspaces/.
5. Открыть дашборд Streamlit на порту 8501.
