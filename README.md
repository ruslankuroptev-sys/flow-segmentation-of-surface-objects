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
2. Скачать модель DeepLabV3+ по ссылке https://disk.yandex.ru/d/fMLWMvtbe0T-Dg
3. Запустить контейнеры: `docker-compose up -d`.
4. Запустить продюсер данных `producer.ipynb` через ноутбук по адресу http://localhost:8888/lab/workspaces/.
5. Запустить спарк `spark.ipynb` через ноутбук по адресу http://localhost:8888/lab/workspaces/.
6. Открыть дашборд Streamlit на порту 8501.
