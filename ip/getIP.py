"""
ip代理请求
"""
import re
from typing import List, Dict, Any

from cache.meta_cache import MetaCache
from .base import BaseRequestClient
from schemas.proxy import KDL_Proxy



class BaseProxyApi():
    """ 快代理api接口 """
    Exception_cls = Exception

    @staticmethod
    def _get_params(**kwargs) -> Dict[str, Any]:
        """ 构造请求参数 """
        pass

    @staticmethod
    def _parse_area_str(*, area_resp: str) -> str:
        """ 解析快代理的地区信息，返回具体的地区编码

        快代理的地区信息比较乱。主要分为下面2中
            1. 江苏省扬州市 联通
            2. 中国 江苏省 扬州市 联通
            3. 北京市北京市  阿里云
            4. 中国 北京市 北京市 阿里云
        @param area_resp: kdl返回的地区信息
        """
        area_resp = area_resp.rsplit(' ')[0]  # 去除 联通/电信/阿里云 等运营商信息
        area_resp.replace(' ', '')   # 去除所有空格
        if area_resp.startswith('中国'):
            area_resp = area_resp[2:]

        # 直辖市比较难处理，直接做特殊处理了
        municipality_codes = {
            '北京': '11',
            '天津': '12',
            '上海': '31',
            '重庆': '50',
        }
        for municipality_name in municipality_codes:
            if municipality_name in area_resp:
                return municipality_codes[municipality_name]

        m = re.match(r'^(\w+[自治区|省])$', area_resp)
        if m:
            pro, city = m.group(1), ''
            return MetaCache.get_code(pro, city)
        m = re.match(r'(\w+[自治区|省])(\w+[地区|自治州|市])\w*', area_resp)
        if m:
            pro, city = m.group(1), m.group(2)
            return MetaCache.get_code(pro, city)
        return ''

    @classmethod
    def get_proxy(cls, *args, **kwargs) -> List[KDL_Proxy]:
        """ 获取开放代理ip """
        pass