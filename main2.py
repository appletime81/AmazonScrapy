import requests
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


def analyze_html(html):
    star_number = html.find_all(attrs={"class": "a-icon-alt"})  # 找評價
    pprint(star_number)


if __name__ == "__main__":
    html = get_html(
        "https://www.amazon.com/s?k=%E6%89%8B%E6%A9%9F&i=mobile&rh=n%3A7072561011%2Cp_36%3A14674873011%2Cp_72%3A2491150011&dc&language=zh_TW&qid=1649076307&rnid=2491147011&ref=sr_nr_p_72_2&page=2 "
    )
    # print(html.prettify())
    analyze_html(html)
