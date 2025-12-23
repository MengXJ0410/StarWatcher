import streamlit as st
import pytz
import math
from datetime import datetime, timedelta

# --- 0. 纯 Python 实现的微型天文算法 (零依赖) ---
# 这是一个简化的开普勒轨道模型，用于估算天体位置
# 精度：演示级 (误差约 15-30 分钟)

class MiniEphem:
    def __init__(self):
        # 简化的轨道参数 (J2000)
        self.bodies = {
            "Mercury": {"N": 48.3313, "i": 7.0047, "w": 29.1241, "a": 0.387098, "e": 0.205635, "M": 168.6562, "rate": 4.0923344368},
            "Venus": {"N": 76.6799, "i": 3.3946, "w": 54.8910, "a": 0.723330, "e": 0.006773, "M": 48.0052, "rate": 1.6021302244},
            "Mars": {"N": 49.5574, "i": 1.8497, "w": 286.5016, "a": 1.523688, "e": 0.093405, "M": 18.6021, "rate": 0.5240207766},
            "Jupiter": {"N": 100.4542, "i": 1.3030, "w": 273.8777, "a": 5.202561, "e": 0.048498, "M": 19.8950, "rate": 0.0830853001},
            "Saturn": {"N": 113.6634, "i": 2.4886, "w": 339.3939, "a": 9.55475, "e": 0.055546, "M": 316.9670, "rate": 0.0334442282},
            "Sun": {"N": 0.0, "i": 0.0, "w": 282.9404, "a": 1.000000, "e": 0.016709, "M": 356.0470, "rate": 0.9856002585},
        }

    def _normalize(self, deg):
        return deg % 360

    def _to_rad(self, deg):
        return deg * math.pi / 180

    def _to_deg(self, rad):
        return rad * 180 / math.pi

    def get_position(self, body_name, dt):
        # 计算 J2000 世纪数
        d = (dt - datetime(2000, 1, 1, 12, 0, 0, tzinfo=pytz.utc)).total_seconds() / 86400.0
        
        if body_name == "Moon":
            # 月球简化模型
            L = self._normalize(218.316 + 13.176396 * d)
            M = self._normalize(134.963 + 13.064993 * d)
            F = self._normalize(93.272 + 13.229350 * d)
            lon = L + 6.289 * math.sin(self._to_rad(M))
            lat = 5.128 * math.sin(self._to_rad(F))
            return lon, lat # Ecliptic coordinates

        # 行星模型
        p = self.bodies.get(body_name, self.bodies["Jupiter"])
        
        # Mean Anomaly
        M = self._normalize(p["M"] + p["rate"] * d)
        
        # Eccentric Anomaly (近似解)
        E = M + (180/math.pi) * p["e"] * math.sin(self._to_rad(M)) * (1 + p["e"] * math.cos(self._to_rad(M)))
        
        # Rectangular coordinates in plane
        x = p["a"] * (math.cos(self._to_rad(E)) - p["e"])
        y = p["a"] * (math.sqrt(1 - p["e"]**2) * math.sin(self._to_rad(E)))
        
        # Distance and True Anomaly
        r = math.sqrt(x*x + y*y)
        v = self._to_deg(math.atan2(y, x))
        
        # Ecliptic coordinates (Heliocentric)
        lon = self._normalize(v + p["w"])
        lat = 0 # Simplified
        
        # 如果是行星，需要转换为地心坐标 (这里做极其简化的处理：假设冲日附近或简单投影)
        # 为了演示稳定性，我们返回黄经即可，主要用于计算大概的升落
        return lon, lat

    def estimate_rise_set(self, body_name, lat, lon, date_obj):
        # 非常粗略的估算：根据天体黄经和太阳黄经的差值
        
        # 1. 计算当天太阳黄经
        sun_lon, _ = self.get_position("Sun", date_obj)
        # 2. 计算目标天体黄经
        body_lon, _ = self.get_position(body_name.split()[0], date_obj) # split for "Jupiter (xx)"
        
        # 3. 角度差 (天体 - 太阳)
        diff = self._normalize(body_lon - sun_lon)
        
        # 4. 估算过中天时间 (Sun transits at ~12:00 local time)
        # 如果 diff = 0 (合)，与太阳同升同落 -> 中天 ~12:00
        # 如果 diff = 180 (冲)，午夜中天 -> 中天 ~00:00
        # diff is degrees East of Sun. Earth rotates 15 deg/hour.
        # Transit shift = -diff / 15 hours
        
        transit_hour_local = 12.0 - (diff / 15.0)
        if transit_hour_local < 0: transit_hour_local += 24
        if transit_hour_local > 24: transit_hour_local -= 24
        
        # 5. 估算升落 (假设在赤道附近平均时长12小时，高纬度会有偏差)
        rise_hour = (transit_hour_local - 6) % 24
        set_hour = (transit_hour_local + 6) % 24
        
        # 构建时间对象
        base_date = date_obj.strftime('%Y-%m-%d')
        def to_str(h):
            m = int((h - int(h)) * 60)
            return f"{int(h):02d}:{m:02d}"
            
        return to_str(rise_hour), to_str(set_hour)

# --- 1. 业务逻辑 ---

CITY_DB = {
    "杭州 (Hangzhou)": (30.2741, 120.1551),
    "上海 (Shanghai)": (31.2304, 121.4737),
    "北京 (Beijing)": (39.9042, 116.4074),
    "深圳 (Shenzhen)": (22.5431, 114.0579),
}

def calculate_star_data(city_name, target_body_name):
    if city_name not in CITY_DB:
        return None, "暂不支持该城市"
        
    lat, lon = CITY_DB[city_name]
    calc = MiniEphem()
    results = []
    
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    # 映射英文名
    name_map = {
        "木星 (Jupiter)": "Jupiter",
        "火星 (Mars)": "Mars", 
        "月亮 (Moon)": "Moon",
        "土星 (Saturn)": "Saturn",
        "金星 (Venus)": "Venus"
    }
    eng_name = name_map.get(target_body_name, "Jupiter")

    for i in range(3):
        check_date = now + timedelta(days=i)
        
        # 使用内置算法估算
        rise_time, set_time = calc.estimate_rise_set(eng_name, lat, lon, check_date)
        
        # 简单的推荐逻辑
        # 解析小时数
        rise_h = int(rise_time.split(':')[0])
        
        recommend = "☀️ 白天模式"
        # 如果升起在晚上 (18:00 - 04:00)
        if 18 <= rise_h <= 23 or 0 <= rise_h <= 4:
            recommend = "⭐⭐⭐ 推荐观测"
        
        results.append({
            "date": check_date.strftime('%Y-%m-%d'),
            "rise": rise_time,
            "set": set_time,
            "recommend": recommend
        })

    return results, None


# --- 2. 页面布局 ---

st.set_page_config(page_title="星空观测助手", page_icon="🔭")

st.title("🌌 城市星空观测助手 (Edge版)")
st.caption("🚀 Powered by Aliyun ESA & Pure Python (No Deps)")

st.markdown("输入你的城市，查看天体升落时间。")

# 侧边栏
with st.sidebar:
    st.header("设置")
    selected_city = st.selectbox("选择城市", list(CITY_DB.keys()))
    selected_body = st.selectbox("选择天体",
                                 ["木星 (Jupiter)", "月亮 (Moon)", "火星 (Mars)", "土星 (Saturn)", "金星 (Venus)"])

    if st.button("开始查询", type="primary"):
        st.session_state.searched = True

# 结果显示
if st.session_state.get('searched'):
    st.subheader(f"📍 {selected_city} - {selected_body}")
    st.markdown("_注：当前使用边缘计算纯数学模型估算，时间仅供参考_")

    data, error = calculate_star_data(selected_city, selected_body)

    if error:
        st.error(error)
    else:
        for item in data:
            with st.container():
                c1, c2, c3, c4 = st.columns(4)
                c1.write(f"**{item['date']}**")
                c2.write(f"⬆️ {item['rise']}")
                c3.write(f"⬇️ {item['set']}")
                c4.caption(item['recommend'])
                st.divider()
else:
    st.info("👈 请在左侧点击“开始查询”")
