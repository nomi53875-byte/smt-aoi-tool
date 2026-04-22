import streamlit as st

st.set_page_config(page_title="SMT 工具", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✨ 介面已精簡：目前為純淨模式，僅顯示下載按鈕。")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        output_rows = []
        seen = set()
        
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                try:
                    # 格式 A (BNG/BAG)
                    d, x, y, a, n = parts[0].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[2].strip()
                    float(x), float(y)
                except:
                    try:
                        # 格式 B (舊格式)
                        d, x, y, a, n = parts[5].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[7].strip()
                        float(x), float(y)
                    except: continue

                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                    if d not in seen and "基准" not in line:
                        output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

        if output_rows:
            st.info(f"✅ 解析完成！共計 {len(output_rows)} 個零件。")
            st.download_button(
                label="📥 點此下載轉檔後的 TXT 檔案",
                data="\r\n".join(output_rows),
                file_name=f"{uploaded_file.name.split('.')[0]}.txt",
                mime='text/plain',
                use_container_width=True
            )
        else:
            st.error("❌ 找不到有效的零件資料。")
    except Exception as e:
        st.error(f"🚨 處理失敗: {e}")
