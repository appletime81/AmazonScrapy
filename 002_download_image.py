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
        attrs={"class": "a-section aok-relative s-image-square-aspect"}
    )  # 找圖片
    for img_src in img_srcs:
        img_src = img_src.find_all(attrs={"class": "s-image"})
        img_src_list.append(img_src[0]["srcset"].split(" ")[-2])

    if price_threshold_max is not None and price_threshold_min is not None:
        price_flag = True
    if star_threshold_max is not None and star_threshold_min is not None:
        star_flag = True

    for star, price, img_src in zip(star_number, prices, img_src_list):
        tmp_star = star
        tmp_price = price
        tmp_img_src = img_src
        if price_flag and float(price_threshold_min) <= float(price) <= float(
            price_threshold_max
        ):
            tmp_price = price
        if star_flag and float(star_threshold_min) <= float(star) <= float(
            star_threshold_max
        ):
            tmp_star = star

        if star_flag or price_flag:
            star_list.append(tmp_star)
            price_list.append(tmp_price)
            img_url_list.append(tmp_img_src)
        else:
            star_list.append(star)
            price_list.append(price)
            img_url_list.append(tmp_img_src)
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


if __name__ == "__main__":
    run_flag = True
    print("******* q: 離開程式 *******")

    while run_flag:
        key_word = input("請輸入搜尋關鍵字: ")
        if key_word == "q":
            run_flag = False
        elif len(key_word) == 0:
            print("請輸入關鍵字")
        else:
            if run_flag:
                html = get_html(f"https://www.amazon.com/s?k={key_word}")
                # https://www.amazon.com/s?k=%E6%89%8B%E6%A9%9F&i=mobilee&rh=n%3A7072561011%2Cp_36%3A14674873011%2Cp_72%3A2491150011&dc&language=zh_TW&qid=1649076307&rnid=2491147011&ref=sr_nr_p_72_2
                star_list, price_list, img_url_list = analyze_html(html)
                # save_as_csv(key_word, star_list, price_list, img_url_list)
