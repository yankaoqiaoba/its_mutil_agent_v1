import math


def bd09mc_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    """
    [工具函数] 百度墨卡托坐标 (BD09MC) 转 百度经纬度 (BD09)
    百度地图 IP 定位 API 返回的是墨卡托坐标，导航 API 需要经纬度，因此必须转换。
    来源：https://github.com/wandergis/coordTransform_py/blob/master/coordTransform_utils.py
    """
    x = lng
    y = lat

    # 1. 简单校验：如果坐标值过小，视为无效坐标（通常在中国境外或解析错误）
    if abs(y) < 1e-6 or abs(x) < 1e-6:
        return (0.0, 0.0)

    # 2. 核心算法：墨卡托平面坐标转球面经纬度
    lng = x / 20037508.34 * 180
    lat = y / 20037508.34 * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)

    return (lng, lat)


if __name__ == '__main__':
    print(bd09mc_to_bd09(12939686.32, 4871085.09))