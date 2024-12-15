from data_processor import read_data, sort_data, group_data, write_data
from event_processor import process_group
import pandas as pd


# Чтение данных
df = read_data('sources_dataset.csv')

# Сортировка данных
df = sort_data(df)

# Группировка данных
grouped = group_data(df)

# Обработка каждой группы
final_results = []
for name, group in grouped:
    final_results.extend(process_group(group))

# Преобразование результатов в DataFrame
final_df = pd.DataFrame(final_results)

# Запись результатов в файл
write_data(final_df, 'processed_dataset.csv')
