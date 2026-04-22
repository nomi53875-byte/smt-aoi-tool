import streamlit as st
import pandas as pd
import io

# 網頁標題與設定
st.set_page_config(page_title="SMT AOI 萬用轉檔工具", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✨ 介面已精簡：目前為純淨模式，僅顯示下載按鈕。")

# 檔案上傳
uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取內容
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen_designators = set()
        
        for line in lines:
            line = line.strip()
            if not line: continue
            parts = line.split(',')
            
            if len(parts) >= 6:
                try:
                    # 格式 A (BNG/BAG)：Ref=0, X=3, Y=4, Angle=5, Name=2
                    designator = parts[0].strip()
                    x, y, angle, part_no = parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[2].strip()
                    float(x), float(y) 
                except (ValueError, IndexError):
                    try:
                        # 格式 B (舊格式)：Ref=5, X=1, Y=2, Angle=3, Name=7
                        designator = parts[5].strip()
                        x, y, angle, part_no = parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[7].strip()
                        float(x), float(y) 
                    except (ValueError, IndexError):
                        continue 

                if designator and not any(k in designator for k in ["参考号", "库", "標示符", "Designator"]):
                    if designator not in seen_designators and "基准" not in line:
                        row = f"{designator}\t{x}\t{y}\t{angle}\tT\t{part_no}"
                        output_rows.append(row)
                        seen_designators.add(designator)

        if output_rows:
            base_name = uploaded_file.name.rsplit('.', 1)[0]
            new_filename = f"{base_name}.txt"
            
            # 僅顯示成功資訊
            st.info(f"✅ 解析完成！共計 {len(output_rows)} 個零件。")
            
            # 顯示下載按鈕
            st.download_button(
                label="📥 點此下載轉檔後的 TXT 檔案",
                data="\r\n".join(output_rows),
                file_name=new_filename,
                mime='text/plain',
                use_container_width=True
            )
            # 這裡之後沒有任何 st.text 指令，所以下方絕對會是乾淨的
            
        else:
            st.error("❌ 無法解析此檔案，請確認內容格式是否有變動。")
            
    except Exception as e:
        st.error(f"🚨 處理失敗: {e}")
