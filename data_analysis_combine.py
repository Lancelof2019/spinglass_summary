import pandas as pd
import os
import argparse

def combine_csv_files(directory, file_pattern):
    # 创建一个空的DataFrame用于存储合并的数据
    combined_df = pd.DataFrame()

    # 遍历目录中的所有CSV文件
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and file_pattern in filename:
            # 读取CSV文件
            df = pd.read_csv(os.path.join(directory, filename))
            # 将CSV文件的数据添加到combined_df中
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # 将合并后的数据写入一个新的CSV文件
    output_file = os.path.join(directory, str(file_pattern)+'analysis_cancers_combined_data.csv')
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine CSV files in a directory.')
    parser.add_argument('directory', type=str, help='Directory containing the CSV files')
    parser.add_argument('file_pattern', type=str, help='File name pattern to match')

    args = parser.parse_args()

    combine_csv_files(args.directory, args.file_pattern)
