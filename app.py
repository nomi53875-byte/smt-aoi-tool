import streamlit as st
import pandas as pd
import io

# 網頁基本設定
st.set_page_config(page_title="SMT AOI 座標轉檔工具", layout="centered")

st.title("🚀 SMT AOI 自動轉檔工具")
st.write("請上傳 `.aoi` 原始檔，系統將自動過濾重複項、移除標題並轉換格式。")

# 檔案上傳區塊
uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取上傳的內容
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen_designators = set() # 用於去重複
        
        # 核心處理邏輯
        for line in lines:
            parts = line.strip().split(',')
            
            if len(parts) > 9:
                designator = parts[5].strip()
                part_type = parts[9].strip()
                
                # 過濾條件：
                # 1. 標示符要有資料 2. 排除標題字眼 3. 排除基準點 4. 排除重複
                if designator and "标示符" not in line and "展开" not in line and "基准" not in part_type:
                    if designator not in seen_designators:
                        x = parts[1].strip()
                        y = parts[2].strip()
                        angle = parts[3].strip()
                        part_no = parts[7].strip()
                        
                        # 組合為 Tab 隔開的格式
                        row = f"{designator}\t{x}\t{y}\t{angle}\tT\t{part_no}"
                        output_rows.append(row)
                        seen_designators.add(designator)
        
        if output_rows:
            # 準備下載內容，強制使用 Windows 換行符號
            final_txt = "\r\n".join(output_rows)
            
            st.success(f"✅ 處理完成！共有 {len(output_rows)} 個唯一零件。")
            
            # 下載按鈕
            st.download_button(
                label="📥 下載轉換後的 TXT 檔",
                data=final_txt,
                file_name=uploaded_file.name.replace('.aoi', '.txt'),
                mime='text/plain'
            )
            
            # 預覽介面
            st.write("---")
            st.write("🧪 資料預覽 (前5筆)：")
            st.text("\n".join(output_rows[:5]))
            
        else:
            st.warning("⚠️ 檔案中找不到符合條件的數據。")
            
    except Exception as e:
        st.error(f"🚨 發生錯誤: {e}")
