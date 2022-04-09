import requests
import re
import os
import pandas as pd

from bs4 import BeautifulSoup
from pprint import pprint


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 "
        "Safari/537.36",
        "cookie": "csm-sid=085-7302629-8217554; x-amz-captcha-1=1649032182195437; "
        "x-amz-captcha-2=8Z6ZUV0aCWlfLHRBgY+vZg==; session-id=144-8672869-0728166; "
        'session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_TW; sp-cdn="L5Z9:TW"; '
        "ubid-main=131-8922267-8264550; av-timezone=Asia/Taipei; "
        "session-token=iDjktDfKoNs2fxlf4Qz8mA20PwDI0BoaLA7oTpvNq2w4gdQJXC/Cu+4PKhUcMBm2EBIjf"
        "+kdZk8Wt21W5Ds4ClERYx192zX3ZIYKLd9auFNQ2UpGPWOmNQDEQDQrkTD8V/jAL44F"
        "/swHHSrSkiJip7fvlms9cK7J8kUHTCoh8yBxr9rvh6RCwnTSeO8HzEEJ; "
        "csm-hit=tb:s-HGD823PGAV42BVCTHP8A|1649076709755&t:1649076710658&adb:adblk_no",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def analyze_html(
    html,
    price_threshold_max=None,
    price_threshold_min=None,
    star_threshold_max=None,
    star_threshold_min=None,
):
    # record product information
    star_list = list()
    price_list = list()
    img_url_list = list()
    price_flag = False
    star_flag = False

    img_src_list = list()
    star_number = [
        re.search(r"\d.\d", item.text).group()
        for item in html.find_all(attrs={"class": "a-icon-alt"})
    ]  # 找評價
    prices = html.find_all(attrs={"class": "a-price-whole"})  # 找價格
    price_fractions = html.find_all(attrs={"class": "a-price-fraction"})  # 找價格小數點

    for i, (price, price_fraction) in enumerate(zip(prices, price_fractions)):
        tmp_price = (
            re.search(r"\d+", price.text).group()
            + "."
            + re.search(r"\d+", price_fraction.text).group()
        )
        prices[i] = tmp_price

    img_srcs = html.find_all(
        attrs={
            # "class": "a-section aok-relative s-image-fixed-height"
            "class": "a-section aok-relative s-image-square-aspect"  # 如果發現無抓取到任何資料請"改用上面被註解那行，此行註解掉"
        }
    )  # 找圖片
    for img_src in img_srcs:
        img_src = img_src.find_all(attrs={"class": "s-image"})
        img_src_list.append(img_src[0]["srcset"].split(" ")[-2])

    print(
        "-----------------------------------------------------------------------------------"
    )
    for star, price, img_src in zip(star_number, prices, img_src_list):
        if (float(price_threshold_min) <= float(price) <= float(price_threshold_max)) and (float(star_threshold_min) <= float(star) <= float(star_threshold_max)):
            star_list.append(star)
            price_list.append(price)
            img_url_list.append(img_src)

        print("評價:", star)
        print("價格:", price)
        print("圖片:", img_src)
    print(f"{len(star_list)}個商品"), print(f"{len(price_list)}個商品"), print(
        f"{len(img_url_list)}個商品"
    )
    return star_list, price_list, img_url_list


def save_as_csv(key_word, star_list, price_list, img_url_list):
    #  建立資料夾
    if not os.path.isdir(f"{key_word}"):
        os.mkdir(f"{key_word}")

    # set file name list
    file_name_list = list()
    for i in range(img_url_list.__len__()):
        file_name_list.append(f"{key_word} {i + 1}.jpg")

    data_dict = {
        "圖片名稱": file_name_list,
        "評價": star_list,
        "價格": price_list,
        "圖片url": img_url_list,
    }
    df = pd.DataFrame(data_dict)
    df.to_csv(f"{key_word}/amazon_data.csv", index=False, encoding="utf-8-sig")


def get_page_numbers(html):
    page_numbers = html.find(attrs={"class": "s-pagination-item s-pagination-disabled"})
    return page_numbers.text


if __name__ == "__main__":
    key_word = "kettle"
    folder_name = "kettle"
    price_threshold_max = 20  # 設定價格最大值
    price_threshold_min = 10  # 設定價格最小值
    star_threshold_max = 5  # 設定評價最大星數
    star_threshold_min = 0  # 設定評價最小星數
    target_url = f"https://www.amazon.com/s?k={key_word}"  # 可直接更換為大類的網址或任一搜尋結果頁面
    page_numbers = get_page_numbers(get_html(target_url))
    page_numbers = int(page_numbers)
    all_star_list = list()
    all_price_list = list()
    all_img_url_list = list()
    for i in range(page_numbers):
        html = get_html(f"{target_url}&page={i + 1}")
        star_list, price_list, img_url_list = analyze_html(
            html,
            price_threshold_max,
            price_threshold_min,
            star_threshold_max,
            star_threshold_min,
        )
        all_star_list.extend(star_list)
        all_price_list.extend(price_list)
        all_img_url_list.extend(img_url_list)
    print(len(all_star_list))
    print(len(all_price_list))
    print(len(all_img_url_list))
    save_as_csv(folder_name, all_star_list, all_price_list, all_img_url_list)
