1. Предварительные требования
- **Python ≥ 3.9**
- **Git**
- **Jupyter Notebook** или **JupyterLab**
- Свободное место: **≈ 300 МБ** (датасет + обработанные данные)

⸻

2. Подготовка окружения

# Клонировать датасет RuReviews
git clone https://github.com/sismetanin/rureviews.git

# Вернуться в корень лабораторной
cd your_project_root/

# Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# Обновить pip и установить зависимости
pip install --upgrade pip
pip install pandas tqdm langdetect regex matplotlib seaborn pyarrow fastparquet wordcloud
pip install jupyterlab


⸻

3. Запуск ноутбука
	1.	Откройте Jupyter Lab:
jupyter lab
	2.	В интерфейсе откройте файл
notebooks/data_prep.ipynb.
	3.	Выполните ячейки по порядку или через Run All Cells.

⸻

4. Что делает ноутбук

1	Загружает CSV из RuReviews
2	Переименовывает поля и очищает тексты	память
3	Определяет язык, удаляет шум
4	Проводит EDA и визуализацию	графики в ноутбуке
5	Создаёт sample для ручной разметки
6	Экспортирует очищенные данные
7	Формирует отчёт о качестве


⸻

5. Проверка результатов

После успешного выполнения в корне проекта появятся:

data/
 └── processed/
     ├── reviews_processed.parquet
     └── annotation_sample.csv
reports/
 └── quality_report.json

Проверить содержимое:

import pandas as pd
df = pd.read_parquet("data/processed/reviews_processed.parquet")
print(df.head())


⸻

6. (Необязательно) Масштабная предобработка через Spark

Если требуется распределённая очистка:

spark-submit --master local[8] src/preprocessing/spark_preprocess.py \
    rureviews/women-clothing-accessories.3-class.balanced.csv \
    data/processed/reviews_spark.parquet


⸻

7. Отчёт о качестве данных

Файл reports/quality_report.json создаётся автоматически и содержит ключевые показатели:

{
  "n_total": 90000,
  "lang_dist": {"ru": 89990, "unknown": 10},
  "avg_words": 47.8,
  "rating_dist": {"positive": 30000, "neutral": 30000, "negative": 30000}
}


