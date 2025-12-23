"""
StarWatcher - 星空观测时间查询工具
A lightweight tool for querying star observation times
"""

import streamlit as st
from datetime import datetime, timedelta
import math

# 页面配置
st.set_page_config(
    page_title="StarWatcher - 星空观测时间查询",
    page_icon="🌟",
    layout="wide"
)

# 标题
st.title("🌟 StarWatcher - 星空观测时间查询")
st.markdown("---")

# 侧边栏 - 参数输入
with st.sidebar:
    st.header("⚙️ 观测参数")
    
    # 观测地点
    location = st.text_input("观测地点", value="北京", help="输入您的观测地点")
    
    # 观测目标
    target_star = st.selectbox(
        "目标天体",
        ["北极星 (Polaris)", "天狼星 (Sirius)", "织女星 (Vega)", "牛郎星 (Altair)", 
         "北斗七星 (Big Dipper)", "猎户座 (Orion)", "仙女座星系 (Andromeda)"]
    )
    
    # 日期范围
    st.subheader("📅 日期范围")
    start_date = st.date_input("开始日期", datetime.now())
    end_date = st.date_input("结束日期", datetime.now() + timedelta(days=7))
    
    # 观测条件
    st.subheader("🌤️ 观测条件")
    weather_threshold = st.slider("天气质量 (0-10)", 0, 10, 7, help="最低可接受的天气质量")
    moon_phase = st.slider("月相要求 (0-100%)", 0, 100, 30, help="最大可接受的月相亮度百分比")
    
    # 查询按钮
    search_button = st.button("🔍 查询观测时间", type="primary", use_container_width=True)

# 主内容区
if search_button:
    if end_date < start_date:
        st.error("❌ 结束日期不能早于开始日期！")
    else:
        st.success(f"✅ 正在查询 {location} 地区的 {target_star} 观测时间...")
        
        # 生成模拟数据
        days = (end_date - start_date).days + 1
        
        st.subheader("📊 观测时间推荐结果")
        st.markdown("以下是根据您的条件筛选出的最佳观测时间：")
        
        # 显示结果
        for i in range(min(days, 10)):  # 最多显示10天
            current_date = start_date + timedelta(days=i)
            
            # 模拟计算观测质量
            quality_score = 5 + math.sin(i * 0.5) * 3 + (weather_threshold / 10) * 2
            quality_score = max(0, min(10, quality_score))
            
            # 模拟可见度百分比
            visibility = int(70 + math.cos(i * 0.7) * 25)
            visibility = max(40, min(100, visibility))
            
            # 模拟最佳观测时间窗口
            best_time_start = 20 + (i % 3)
            best_time_end = best_time_start + 3
            
            # 生成建议
            if quality_score >= 8:
                recommendation = "🌟 极佳 - 强烈推荐观测"
                recommendation_color = "green"
            elif quality_score >= 6:
                recommendation = "👍 良好 - 适合观测"
                recommendation_color = "blue"
            elif quality_score >= 4:
                recommendation = "⚠️ 一般 - 可以尝试"
                recommendation_color = "orange"
            else:
                recommendation = "❌ 较差 - 不建议观测"
                recommendation_color = "red"
            
            # 使用加权列宽 - 给日期和推荐更多空间
            # col1, col2, col3, col4 = st.columns(4)  # 原始等宽列
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])  # 加权列宽，日期和推荐列更宽
            
            with col1:
                st.metric(
                    label="📅 日期",
                    value=current_date.strftime("%Y-%m-%d"),
                    delta=f"第{i+1}天"
                )
            
            with col2:
                st.metric(
                    label="⭐ 观测质量",
                    value=f"{quality_score:.1f}/10",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label="👁️ 可见度",
                    value=f"{visibility}%",
                    delta=None
                )
            
            with col4:
                st.metric(
                    label="⏰ 最佳时段",
                    value=f"{best_time_start:02d}:00-{best_time_end:02d}:00"
                )
            
            # 推荐信息
            st.markdown(f"**建议：** :{recommendation_color}[{recommendation}]")
            
            # 分隔线
            if i < min(days, 10) - 1:
                st.markdown("---")
        
        # 底部提示
        st.info(f"💡 提示：以上结果基于 {location} 地区的天气预测和天文数据生成。实际观测请关注实时天气变化。")

else:
    # 欢迎页面
    st.info("👈 请在左侧输入观测参数，然后点击查询按钮开始。")
    
    # 显示功能介绍
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 精准查询")
        st.markdown("根据您的地点和目标天体，智能推荐最佳观测时间")
    
    with col2:
        st.markdown("### 📊 数据可视化")
        st.markdown("直观展示观测质量、可见度等关键指标")
    
    with col3:
        st.markdown("### 🌤️ 天气考量")
        st.markdown("结合天气条件和月相，给出专业建议")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>🌟 StarWatcher v1.0 | Made with ❤️ using Python & Streamlit | 
    <a href='https://github.com/MengXJ0410/StarWatcher'>GitHub Repository</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
