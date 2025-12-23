import streamlit as st
import ephem
import pytz
from datetime import datetime, timedelta

# --- 1. 核心逻辑 ---

CITY_DB = {
    "杭州": (30.2741, 120.1551),
    "Hangzhou": (30.2741, 120.1551),
    "上海": (31.2304, 121.4737),
    "Shanghai": (31.2304, 121.4737),
    "北京": (39.9042, 116.4074),
    "Beijing": (39.9042, 116.4074),
    "深圳": (22.5431, 114.0579),
    "Shenzhen": (22.5431, 114.0579),
    "广州": (23.1291, 113.2644),
    "Guangzhou": (23.1291, 113.2644)
}

def calculate_star_data(city_name, target_body_name):
    # 获取经纬度
    if city_name in CITY_DB:
        lat, lon = CITY_DB[city_name]
    else:
        return None, "暂不支持该城市"

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 0
    now = datetime.now(pytz.utc)
    observer.date = now

    # 映射天体对象
    body_map = {
        "木星 (Jupiter)": ephem.Jupiter(),
        "火星 (Mars)": ephem.Mars(),
        "月亮 (Moon)": ephem.Moon(),
        "土星 (Saturn)": ephem.Saturn(),
        "金星 (Venus)": ephem.Venus()
    }
    body = body_map.get(target_body_name)
    if body is None:
         return None, "未知天体"

    body.compute(observer)

    # 计算未来3天数据
    results = []
    current_check = now
    local_tz = pytz.timezone('Asia/Shanghai')

    for i in range(3):
        observer.date = current_check
        body.compute(observer)
        try:
            # 计算下一次升起和落下
            rising_ephem = observer.next_rising(body)
            setting_ephem = observer.next_setting(body)
            
            rising = rising_ephem.datetime().replace(tzinfo=pytz.utc).astimezone(local_tz)
            setting = setting_ephem.datetime().replace(tzinfo=pytz.utc).astimezone(local_tz)

            # 简单的逻辑判断：是否适合观测
            is_night = False
            # 粗略判断：如果升起或落下时间在 18:00-06:00 之间
            if rising.hour >= 18 or rising.hour <= 6 or setting.hour >= 18 or setting.hour <= 6:
                is_night = True

            results.append({
                "date": rising.strftime('%Y-%m-%d'),
                "rise": rising.strftime('%H:%M'),
                "set": setting.strftime('%H:%M'),
                "recommend": "⭐⭐⭐ 推荐观测" if is_night else "⭐ 白天可见度低"
            })
            current_check += timedelta(days=1)
        except (ephem.AlwaysUpError, ephem.NeverUpError):
             # 极昼极夜或永不升起
             pass
        except Exception:
             pass

    if not results:
        return None, "该天体近期在地平线以下或无法观测"
        
    return results, None


# --- 2. 页面布局 ---

st.set_page_config(page_title="星空观测助手", page_icon="🔭")

st.title("🌌 城市星空观测助手 (Server版)")
st.caption("🚀 Powered by Docker & Python Ephem")

st.markdown("输入你的城市，查看今晚是否适合观测木星、月亮等天体。")

# 侧边栏输入
with st.sidebar:
    st.header("设置")
    selected_city = st.selectbox("选择城市", list(CITY_DB.keys()))
    selected_body = st.selectbox("选择天体",
                                 ["木星 (Jupiter)", "月亮 (Moon)", "火星 (Mars)", "土星 (Saturn)", "金星 (Venus)"])

    if st.button("开始查询", type="primary"):
        st.session_state.searched = True

# 主界面显示结果
if st.session_state.get('searched'):
    st.subheader(f"📍 {selected_city} - {selected_body} 观测报告")

    data, error = calculate_star_data(selected_city, selected_body)

    if error:
        st.error(error)
    else:
        for day in data:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                col1.metric("日期", day['date'])
                col2.metric("⬆️ 升起", day['rise'])
                col3.metric("⬇️ 落下", day['set'])
                col4.write(f"**{day['recommend']}**")
                st.divider()
else:
    st.info("👈 请在左侧侧边栏选择城市和天体，然后点击“开始查询”")
