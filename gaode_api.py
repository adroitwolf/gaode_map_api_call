import json
import requests


class Gaode():
    def __init__(self,key) -> None:
        super().__init__()
        self.key = key
    
    def requests_url_get(self,url):
        """ 请求url方法get方法 """
        try:
            r = requests.get(url=url, timeout=30)
            if r.status_code == 200:
                return r.text
            return None
        except Exception as ex:
            print(ex)
            return None
    def parse_json(self,content_json):
        """  解析json函数 """
        result_json = json.loads(content_json)
        return result_json
    def get_city_location(self,city):
        url = f"https://restapi.amap.com/v5/place/text?key={self.key}&keywords={city}"
        text = self.requests_url_get(url)
        if text is None:
            return None
        result_json = self.parse_json(text)
        return result_json['pois'][0]['location']
    def get_distance(self,origin,target):
        url = f"https://restapi.amap.com/v3/distance?origins={origin}&destination={target}&key={self.key}&type=1"
        text = self.requests_url_get(url)
        if text is None:
            return None
        result_json = self.parse_json(text)
        return int(result_json['results'][0]['distance']) /1000