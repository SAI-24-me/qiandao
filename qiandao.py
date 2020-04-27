import requests
from PIL import Image
import numpy as np
import time


def qiandao(qiandaoma, yonghu='zijitian'):
    true = np.load("true.npy")
    code = qiandaoma
    x = 17
    token = yonghu
    url_checkin = "https://skl.hdu.edu.cn/api/checkIn/code-check-in?code=" + code
    headers_checkin = {
        "authority": "skl.hdu.edu.cn",
        "method": "GET",
        "path": "api/checkIn/code-check-in?code=" + code,
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://skl.hduhelp.com",
        "referer": "https://skl.hduhelp.com/?token=" + token,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36",
        "x-auth-token": token,
    }
    url_img = "https://skl.hdu.edu.cn/api/checkIn/create-code-img"
    headers_img = {
        "authority": "skl.hdu.edu.cn",
        "method": "GET",
        "path": "/api/checkIn/create-code-img",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://skl.hduhelp.com",
        "referer": "https://skl.hduhelp.com/?token=" + token,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36",
        "x-auth-token": token,
    }

    a = requests.get(url_checkin, headers=headers_checkin)
    b = requests.get(url_img, headers=headers_img)
    with open('yzm.png', 'wb') as f:
        f.write(b.content)
    f.close()
    img = Image.open('yzm.png')
    grey_img = img.convert('L')
    arr = np.array(grey_img)
    arr = 255 - arr
    num = np.split(arr, [x, x * 2, x * 3, x * 4], axis=1)
    ans = ""
    for j in range(4):
        a = []
        for k in range(10):
            a.append((num[j] * true[k]).sum())
        pnum = np.where(a == np.max(a))[0][0]
        ans += str(pnum)
    yanzhengma = ans
    url_yanzhengma = "https://skl.hdu.edu.cn/api/checkIn/valid-code?code=" + yanzhengma
    headers_code = {
        "authority": "skl.hdu.edu.cn",
        "method": "GET",
        "path": "/api/checkIn/valid-code?code=" + yanzhengma,
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://skl.hduhelp.com",
        "referer": "https://skl.hduhelp.com/?token=" + token,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36",
        "x-auth-token": token,
    }

    c = requests.get(url_yanzhengma, headers=headers_code)
    return c.status_code


if __name__ == '__main__':
    sum = 0
    test = 30
    for i in range(1, test):
        if (qiandao("1234") == 401):
            sum += 1
        time.sleep(2)
        print("实验：", i, "次", "成功：", sum, "次", "当前成功率:", sum / i)
