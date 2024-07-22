import pandas as pd
import os

def find_max_column_count(input_directory, file_pattern, delimiter=','):
    max_column_count = 0
    for filename in os.listdir(input_directory):
        if file_pattern in filename:
            input_path = os.path.join(input_directory, filename)
            with open(input_path, 'r') as file:
                for line in file:
                    # 计算当前行的列数
                    current_max = len(line.split(delimiter))
                    if current_max > max_column_count:
                        max_column_count = current_max
    return max_column_count

def create_summary_excel(input_directory, output_file_path, file_pattern, delimiter=','):
    # 先找到所有文件中的最大列数
    max_column_count = find_max_column_count(input_directory, file_pattern, delimiter)
    print(f"Maximum column count across files: {max_column_count}")

    # 创建一个Pandas Excel writer，使用xlsxwriter作为引擎
    writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter')

    # 遍历输入目录中所有符合文件模式的文件
    for filename in os.listdir(input_directory):
        if file_pattern in filename:
            input_path = os.path.join(input_directory, filename)

            # 初始化一个空的DataFrame
            df = pd.DataFrame()

            with open(input_path, 'r') as file:
                lines = file.readlines()[1:]
                # 将每一行都拆分成列，形成一个列表的列表
                data = [line.strip().split(delimiter) for line in lines]
                # 补全列，缺少的列用NaN填充
                for row in data:
                    if len(row) < max_column_count:
                        row.extend([pd.NA] * (max_column_count - len(row)))

                # 创建DataFrame
                df = pd.DataFrame(data)

            # 计算每行的列数
            column_count = df.apply(lambda x: x.count(), axis=1)

            # 将列数添加为新列，放在第一列
            df.insert(0, 'Column_Count', column_count)

            # 获取文件名的前缀作为sheet的名称，假设文件名形式为 "PREFIX_anything.csv"
            sheet_name = filename.split('_')[0]

            # 将DataFrame写入为一个Excel的sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # 保存Excel文件
    writer.close()

    print(f"All files processed and saved to {output_file_path}")

# 指定输入目录和输出文件的路径
input_directory = '/projappl/project_2010541/data/spinglass'  # 替换为你的输入目录路径
output_file_path = '/projappl/project_2010541/data/spinglass/summary_data_analysis.xlsx'  # 替换为你的输出文件路径

# 文件模式，例如包含 'survival_analysis_results14.csv' 的文件
file_pattern = 'best01_output'

# 调用函数
create_summary_excel(input_directory, output_file_path, file_pattern)
