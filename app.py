import streamlit as st
import pandas as pd
import io

# 網頁標題與設定
st.set_page_config(page_title="SMT AOI 萬用轉檔工具", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具 (自動排版糾錯)")
st.write("此版本已修正：自動偵測標題行、防止首行遺失、解決不同排版欄位錯位問題。")

# 檔案上傳
uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取內容，使用 gbk 編碼
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen_designators = set()
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            parts = line.split(',')
            
            # 偵測這行是否為有效零件行
            if len(parts) >= 6:
                # 針對新檔案 (BNG/BAG系列)：參考號在 index 0, X在 3, Y在 4, 角度在 5, 元件名在 2
                # 針對舊檔案：參考號在 index 5, X在 1, Y在 2, 角度在 3, 元件名在 7
                
                # 自動判斷欄位邏輯：
                # 如果 index 3 和 4 都是數字，代表是新格式
                # 如果 index 1 和 2 都是數字，代表是舊格式
                try:
                    # 測試新格式 (BNG/BAG)
                    designator = parts[0].strip()
                    x, y, angle, part_no = parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[2].strip()
                    float(x), float(y) # 驗證是否為數字
                except (ValueError, IndexError):
                    try:
                        # 測試舊格式
                        designator = parts[5].strip()
                        x, y, angle, part_no = parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[7].strip()
                        float(x), float(y) # 驗證是否為數字
                    except (ValueError, IndexError):
                        continue # 兩者都不符，跳過此行 (可能是標題)

                # 過濾：排除中文字標題、重複項、基準點
                if designator and not any(k in designator for k in ["参考号", "库", "標示符", "Designator"]):
                    if designator not in seen_designators and "基准" not in line:
                        row = f"{designator}\t{x}\t{y}\t{angle}\tT\t{part_no}"
                        output_rows.append(row)
                        seen_designators.add(designator)

        if output_rows:
            # 處理檔名
            base_name = uploaded_file.name.rsplit('.', 1)[0]
            new_filename = f"{base_name}.txt"
            
            st.success(f"✅ 轉換成功！處理了 {len(output_rows)} 個零件。")
            
            # 下載按鈕
            st.download_button(
                label="📥 下載轉檔後的 TXT",
                data="\r\n".join(output_rows),
                file_name=new_filename,
                mime='text/plain'
            )
            
            st.write("---")
            st.write("🧪 零件預覽：")
            st.text("\n".join(output_rows[:10]))
        else:
            st.error("❌ 無法解析此檔案，請確認內容格式是否有變動。")
            
    except Exception as e:
        st.error(f"🚨 處理失敗: {e}")
