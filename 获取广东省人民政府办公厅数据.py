import json
import re
import requests
from datetime import datetime


def get_data(i,time_MAX, time_MIN):
    url = 'https://www.gd.gov.cn/gkmlpt/api/all/5?page='+str(i)+'&sid=2'
    cookies = {
        'Path': '/',
        'gkmlfront_session': 'eyJpdiI6Im5RMWZyeGt2K2dTbHFnY2VybmpuNkE9PSIsInZhbHVlIjoiXC9EMHdGNU9KYVI3R1JiYU5ZTk9oNTYyNis5TTNrTm1lK3BqNVVPUU5WNUk0NUJud1RMa0swNW1ZaFwvem9EWmM0IiwibWFjIjoiZjRlYmYzZjdmZTRhZjJhODhiOTdkOWRhZDMzNWM5MmZhZGFkMzI0MjkyN2IzMTE0MGIxYmNmY2YwYzQ5MDY1MSJ9',
        'front_uc_session': 'eyJpdiI6IkRWNk5CY0ZoMWI3ZzJxSk5leEQ3MUE9PSIsInZhbHVlIjoiVkpLcEc3elRUdEMyVytLZ1A5aTJ4Zlh5UFwvMHhBUENRVzZlTU9NWDlObk4wR3J0VmkxY0s4V2hPbUlUXC9xSTJwIiwibWFjIjoiNTE0Yzg0OGIwY2RkNDc4MjFlOTA2OTdkMDI1NGJiZWY4MGY1MjcyYTEwOTc0NjA0NTEwZWEzYTk0NTYzMGJjZCJ9',
    }

    data = {
        'page': str(i),
        'sid': '2'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'Path=/; gkmlfront_session=eyJpdiI6Im5RMWZyeGt2K2dTbHFnY2VybmpuNkE9PSIsInZhbHVlIjoiXC9EMHdGNU9KYVI3R1JiYU5ZTk9oNTYyNis5TTNrTm1lK3BqNVVPUU5WNUk0NUJud1RMa0swNW1ZaFwvem9EWmM0IiwibWFjIjoiZjRlYmYzZjdmZTRhZjJhODhiOTdkOWRhZDMzNWM5MmZhZGFkMzI0MjkyN2IzMTE0MGIxYmNmY2YwYzQ5MDY1MSJ9; front_uc_session=eyJpdiI6IkRWNk5CY0ZoMWI3ZzJxSk5leEQ3MUE9PSIsInZhbHVlIjoiVkpLcEc3elRUdEMyVytLZ1A5aTJ4Zlh5UFwvMHhBUENRVzZlTU9NWDlObk4wR3J0VmkxY0s4V2hPbUlUXC9xSTJwIiwibWFjIjoiNTE0Yzg0OGIwY2RkNDc4MjFlOTA2OTdkMDI1NGJiZWY4MGY1MjcyYTEwOTc0NjA0NTEwZWEzYTk0NTYzMGJjZCJ9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    requests_json =requests.get(url=url, headers=headers, cookies=cookies,json=data).json()
    data_json = json.dumps(requests_json)
    data = json.loads(data_json)
    for articles in data['articles']:
        time_obj = datetime.strptime(articles['created_at'], "%Y-%m-%d %H:%M:%S")

        if time_MIN < time_obj < time_MAX:
            # 获取索引号
            identifier = articles['identifier']
            # 发布机构
            publisher = articles['publisher']
            # 发布日期
            created_at = articles['created_at']
            # 政策标题
            title = articles['title']
            # 政策正文附件链接
            url_data = articles['url']
            # 政策正文文本
            response = requests.get(url=url_data, headers=headers)
            # < p style = "text-align: justify;" >　　经省人民政府同意，现将《广东省突发事件医疗卫生救援应急预案》印发给你们，请认真组织实施。实施过程中遇到的问题，请径向省卫生健康委反映。 < / p >
            requests_text = re.compile('.*?：</p><p style="text-align: justify;">(.*?)</p>', re.DOTALL)
            requests_text = requests_text.findall(response.text)
            print("索引号:" + identifier)
            print("发布机构:" + publisher)
            print("发布日期:" + created_at)
            print("政策标题:" + title)
            print(requests_text)
            print("政策正文附件链接:" + url_data)


def input_time():
    time_range_str = input("输入时间范围格式：(20220101-20230601)")
    # time_range_str = "(20240101-20240110)"

    # 解析时间范围字符串
    start_time_str, end_time_str = time_range_str[1:-1].split("-")
    start_time = datetime.strptime(start_time_str, "%Y%m%d")
    end_time = datetime.strptime(end_time_str, "%Y%m%d")
    return start_time, end_time


if __name__ == '__main__':
    times = input_time()
    for i in range(1, 49):
        get_data(i, times[1], times[0])
