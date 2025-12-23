import ephem
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import pytz

# 【新增】一个简单的中国城市经纬度字典 (离线数据，无需联网，速度快)
CITY_DB = {
    "hangzhou": (30.2741, 120.1551, "中国浙江省杭州市"),
    "杭州": (30.2741, 120.1551, "中国浙江省杭州市"),
    "shanghai": (31.2304, 121.4737, "中国上海市"),
    "上海": (31.2304, 121.4737, "中国上海市"),
    "beijing": (39.9042, 116.4074, "中国北京市"),
    "北京": (39.9042, 116.4074, "中国北京市"),
    "shenzhen": (22.5431, 114.0579, "中国广东省深圳市"),
    "深圳": (22.5431, 114.0579, "中国广东省深圳市"),
    "guangzhou": (23.1291, 113.2644, "中国广东省广州市"),
    "广州": (23.1291, 113.2644, "中国广东省广州市"),
    # 你可以继续添加更多城市...
}


def get_coordinates(city_name):
    """
    优先使用本地字典查找，找不到再尝试联网 (或者直接报错)
    这样在阿里云服务器上非常稳定。
    """
    # 1. 清理输入 (去掉空格，转小写)
    key = city_name.strip().lower()

    # 2. 查本地字典
    if key in CITY_DB:
        return CITY_DB[key]

    # 3. 如果本地没有，为了比赛演示稳定，建议返回一个默认城市或者提示不支持
    # 也可以保留 geopy 作为 fallback，但建议比赛时注释掉，防止卡顿
    # from geopy.geocoders import Nominatim
    # try:
    #     geolocator = Nominatim(user_agent="astro_observer_app", timeout=10)
    #     location = geolocator.geocode(city_name)
    #     if location:
    #         return location.latitude, location.longitude, location.address
    # except:
    #     pass

    return None, None, None

def calculate_viewing_time(city_name, target_body="Jupiter", days=3):
    """
    计算最佳观测时间
    :param city_name: 城市名称 (中文或英文)
    :param target_body: 目标天体 (目前支持 'Jupiter', 'Moon', 'Mars')
    :param days: 预测未来几天
    """
    # 1. 获取经纬度
    lat, lon, address = get_coordinates(city_name)
    if not lat:
        print(f"❌ 找不到城市: {city_name}")
        return

    print(f"📍 定位成功: {address}")
    print(f"   (纬度: {lat:.4f}, 经度: {lon:.4f})\n")

    # 2. 设置观测者 (Observer)
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 0  # 假设海平面，稍微影响不大

    # 获取当前 UTC 时间 (ephem 使用 UTC)
    now = datetime.now(pytz.utc)
    observer.date = now

    # 3. 选择天体
    if target_body.lower() == 'jupiter':
        body = ephem.Jupiter()
        target_name = "木星"
    elif target_body.lower() == 'mars':
        body = ephem.Mars()
        target_name = "火星"
    elif target_body.lower() == 'moon':
        body = ephem.Moon()
        target_name = "月亮"
    else:
        print("暂时只支持木星(Jupiter)、火星(Mars)和月亮(Moon)。")
        return

    print(f"🔭 正在计算 {target_name} 在未来 {days} 天的观测窗口...\n")

    # 4. 循环计算未来几天的升起和落下时间
    current_check_date = now

    found_any = False

    for i in range(days):
        observer.date = current_check_date
        body.compute(observer)

        try:
            # 计算下一次升起和落下时间
            rising = observer.next_rising(body).datetime().replace(tzinfo=pytz.utc)
            setting = observer.next_setting(body).datetime().replace(tzinfo=pytz.utc)

            # 转换为本地时间 (假设中国用户，使用 Asia/Shanghai)
            local_tz = pytz.timezone('Asia/Shanghai')
            rising_local = rising.astimezone(local_tz)
            setting_local = setting.astimezone(local_tz)

            # 简单的逻辑：如果升起时间在晚上 (18:00 - 06:00)，则推荐
            # 注意：这里是一个简化的判断，实际观测还需要考虑太阳是否落下

            fmt = "%Y-%m-%d %H:%M"
            print(f"📅 日期: {rising_local.strftime('%Y-%m-%d')}")
            print(f"   ⬆️ 升起时间: {rising_local.strftime('%H:%M')}")
            print(f"   ⬇️ 落下时间: {setting_local.strftime('%H:%M')}")

            # 判断是否适合观测 (简单判断：升起后或者落下前是在夜里)
            # 这里简化逻辑：只要能升起来，就建议观测，通常木星很亮，晚上都能看
            print(
                f"   ✨ 建议观测时段: {rising_local.strftime('%H:%M')} 到 {setting_local.strftime('%H:%M')} (如果是白天请忽略)")
            print("-" * 30)

            found_any = True

            # 推进到第二天
            current_check_date += timedelta(days=1)

        except ephem.AlwaysUpError:
            print(f"第 {i + 1} 天: {target_name} 全天在地平线以上 (极昼区域?)")
        except ephem.NeverUpError:
            print(f"第 {i + 1} 天: {target_name} 全天在地平线以下，无法观测。")

    if not found_any:
        print("近期无法观测该天体。")


if __name__ == "__main__":
    # 用户输入交互
    city = input("请输入你的城市 (例如: 杭州/Hangzhou): ")
    target = input("请输入你想观测的天体 (Jupiter/Moon/Mars): ") or "Jupiter"

    print("\n" + "=" * 40)
    calculate_viewing_time(city, target)
    print("=" * 40)