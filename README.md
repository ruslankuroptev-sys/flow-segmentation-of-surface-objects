# flow-segmentation-of-surface-objects

D:\MARINE_PIPELINE
├── dataset/             # Исходные данные
│   ├── Detection/       # Данные для обучения YOLO
│   └── Segmentation/    # Данные для DeepLabV3+ (MaSTr1325)
├── data_lake/           # Результаты работы конвейера (Маски и Визуализация)
├── nifi_data/           # Конфигурации Apache NiFi
├── postgres_data/       # База данных метаданных (PostgreSQL)
├── shared_hdfs/         # Распределенное хранилище (Hadoop HDFS)
└── workspace/           # Основная рабочая область
    ├── models/          # Финальные веса моделей
    ├── runs/            # Логи обучения и веса YOLO
    ├── checkpoints/     # Контрольные точки Spark Streaming
    └── *.py / *.ipynb   # Исходный код и ноутбуки
