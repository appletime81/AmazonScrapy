import os
import pandas as pd


def save_img(csv_filename):
    root = os.path.abspath(os.path.dirname(csv_filename)) + "\\"
    df = pd.read_csv(csv_filename)
    urls = df["圖片url"].values
    filenames = df["圖片名稱"].values
    for url, filename in zip(urls, filenames):
        os.system(f"python -m wget {url} -o {root}")
        os.rename(root + url.split("/")[-1], root + filename)


if __name__ == "__main__":
    save_img("紅茶/amazon_data.csv")