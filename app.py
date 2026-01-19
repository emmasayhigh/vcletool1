import streamlit as st
import yt_dlp
import os
import time
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH BAN ĐẦU ---
st.set_page_config(
    page_title="VCLE Download",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. QUẢN LÝ SESSION ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'vi'
if 'show_howto' not in st.session_state:
    st.session_state.show_howto = False

# --- 3. TỪ ĐIỂN NGÔN NGỮ (Đã kiểm tra kỹ key 'best') ---
TRANS = {
    'vi': {
        'title': "VCLE Download",
        'subtitle': "Tải Video TikTok - Facebook - YouTube Đa Nền Tảng",
        'placeholder': "Dán link Video vào đây...",
        'btn_dl': "TẢI XUỐNG NGAY ⬇",
        'format': "Định dạng",
        'quality': "Chất lượng / Bitrate",
        'video': "Video (MP4)",
        'audio': "Âm thanh (MP3)",
        'best': "Tốt nhất (Auto)",  # <--- Key này quan trọng, không được xóa
        'howto_title': "📖 Hướng dẫn",
        'howto_steps': [
            "1. Copy link video TikTok, FB, hoặc YT.",
            "2. Dán vào ô bên dưới.",
            "3. Chọn MP4 (Video) hoặc MP3 (Nhạc).",
            "4. Bấm tải và xem quảng cáo ủng hộ Admin."
        ],
        'wait': "⏳ Đang xử lý... (Vui lòng đợi 3s)",
        'success': "✅ Xong! Lưu file tại đây:",
        'save_btn': "💾 LƯU VỀ MÁY",
        'error': "❌ Lỗi: Link sai hoặc video riêng tư.",
        'ad_wait': "🔥 ĐANG TẢI DỮ LIỆU TỪ MÁY CHỦ..."
    },
    'en': {
        'title': "VCLE Download",
        'subtitle': "Free TikTok - Facebook - YouTube Downloader",
        'placeholder': "Paste Video Link here...",
        'btn_dl': "DOWNLOAD NOW ⬇",
        'format': "Format",
        'quality': "Quality / Bitrate",
        'video': "Video (MP4)",
        'audio': "Audio (MP3)",
        'best': "Best (Auto)",
        'howto_title': "📖 How to use",
        'howto_steps': [
            "1. Copy video link (TikTok, FB, YT).",
            "2. Paste into the box below.",
            "3. Choose MP4 or MP3.",
            "4. Click Download and wait."
        ],
        'wait': "⏳ Processing... (Wait 3s)",
        'success': "✅ Done! Save file:",
        'save_btn': "💾 SAVE FILE",
        'error': "❌ Error: Invalid or private link.",
        'ad_wait': "🔥 DOWNLOADING DATA FROM SERVER..."
    }
}
# Lấy từ điển dựa trên ngôn ngữ đã chọn
T = TRANS[st.session_state.lang]

# --- 4. CSS TỐI ƯU GIAO DIỆN ---
st.markdown("""
<style>
    /* Nền đen */
    .stApp { background-color: #000000 !important; color: #fff !important; }
    header, footer { visibility: hidden !important; }

    /* NAVBAR: Canh chỉnh Help và Language thẳng hàng */
    .nav-container {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 20px; background: #111; border-bottom: 1px solid #333;
    }
    
    /* Nút Help cho đẹp hơn */
    div.stButton > button {
        border-radius: 5px; font-weight: bold;
    }
    
    /* INPUT & BUTTON CHÍNH */
    input.stTextInput {
        background-color: #1a1a1a !important; color: white !important;
        border: 1px solid #333 !important; padding: 25px !important; font-size: 16px;
    }
    .main-btn > button {
        background: linear-gradient(90deg, #ff0050, #00f2ea) !important;
        color: white !important; border: none !important; font-weight: bold !important;
        padding: 15px !important; font-size: 20px !important; width: 100%;
        text-transform: uppercase; margin-top: 28px; /* Căn cho bằng input */
    }
    
    /* KHUNG HELP */
    .howto-box {
        background: #222; padding: 15px; border-radius: 8px;
        border-left: 4px solid #00f2ea; margin-bottom: 20px;
    }
    
    /* Selectbox chỉnh màu đen */
    div[data-baseweb="select"] > div {
        background-color: #222 !important; color: white !important; border-color: #444 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. NAVBAR (ĐÃ SỬA ĐỒNG NHẤT) ---
with st.container():
    c1, c2, c3 = st.columns([3, 5, 2])
    with c1:
        st.markdown(f"### 📥 VCLE Download")
    with c3:
        # Chia cột nhỏ để nút Help và Selectbox nằm cạnh nhau đẹp hơn
        cl_1, cl_2 = st.columns([1, 2], gap="small")
        with cl_1:
            if st.button("❓ Help", use_container_width=True):
                st.session_state.show_howto = not st.session_state.show_howto
        with cl_2:
            # Logic đổi ngôn ngữ
            idx = 0 if st.session_state.lang == 'vi' else 1
            new_lang = st.selectbox("Lang", ["Tiếng Việt", "English"], index=idx, label_visibility="collapsed")
            
            # Cập nhật session state nếu đổi ngôn ngữ
            if new_lang == "Tiếng Việt" and st.session_state.lang != 'vi':
                st.session_state.lang = 'vi'
                st.rerun()
            elif new_lang == "English" and st.session_state.lang != 'en':
                st.session_state.lang = 'en'
                st.rerun()

# --- 6. QUẢNG CÁO HEADER (BANNER NGANG) ---
# ĐÃ GẮN CODE QUẢNG CÁO SỐ 1 (728x90)
components.html("""
<div style="display:flex; justify-content:center; align-items:center; background:#111; height:90px; color:#555; border:1px dashed #444;">
    <script>
      atOptions = {
        'key' : '7cd087fd6ceed9ebc182a8dafcde705c',
        'format' : 'iframe',
        'height' : 90,
        'width' : 728,
        'params' : {}
      };
    </script>
    <script src="https://www.highperformanceformat.com/7cd087fd6ceed9ebc182a8dafcde705c/invoke.js"></script>
</div>
""", height=100)

# --- 7. HIỆN HELP NẾU ĐƯỢC BẤM ---
if st.session_state.show_howto:
    st.markdown(f"""
    <div class="howto-box">
        <b>{T['howto_title']}</b><br>
        {'<br>'.join(T['howto_steps'])}
    </div>
    """, unsafe_allow_html=True)

# --- 8. BỐ CỤC CHÍNH (3 CỘT) ---
col_L, col_M, col_R = st.columns([1, 4, 1])

# ➤ CỘT TRÁI: ADS
# ĐÃ GẮN CODE QUẢNG CÁO SỐ 3 (160x600)
with col_L:
    components.html("""
    <div style="background:#111; height:600px; color:#555; display:flex; justify-content:center; align-items:center; border:1px dashed #444;">
        <script>
          atOptions = {
            'key' : 'a2290a3f17b278ebb0282ecbc8a7d5be',
            'format' : 'iframe',
            'height' : 600,
            'width' : 160,
            'params' : {}
          };
        </script>
        <script src="https://www.highperformanceformat.com/a2290a3f17b278ebb0282ecbc8a7d5be/invoke.js"></script>
    </div>
    """, height=600)

# ➤ CỘT GIỮA: NỘI DUNG
with col_M:
    st.markdown(f"<h1 style='text-align: center'>{T['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #aaa'>{T['subtitle']}</p>", unsafe_allow_html=True)
    
    # Input Link
    url = st.text_input("", placeholder=T['placeholder'])
    
    # ➤ ADS GIỮA (Dưới Input)
    # Tận dụng code số 1 (728x90) vì không có code 468x60 riêng
    components.html("""
    <div style="display:flex; justify-content:center; background:#111; height:90px; align-items:center; color:#555; border:1px dashed #333; overflow:hidden;">
        <script>
          atOptions = {
            'key' : '7cd087fd6ceed9ebc182a8dafcde705c',
            'format' : 'iframe',
            'height' : 90,
            'width' : 728,
            'params' : {}
          };
        </script>
        <script src="https://www.highperformanceformat.com/7cd087fd6ceed9ebc182a8dafcde705c/invoke.js"></script>
    </div>
    """, height=100)
    
    # Tùy chọn (Chia 3 cột cho nút tải nằm cùng hàng)
    c_fmt, c_qual, c_btn = st.columns([1.5, 1.5, 1.5])
    
    with c_fmt:
        fmt = st.selectbox(T['format'], [T['video'], T['audio']])
    
    with c_qual:
        # LOGIC CHỌN CHẤT LƯỢNG (Fix lỗi KeyError: 'best' tại đây)
        if fmt == T['audio']:
            # Nếu là Audio -> Hiện bitrate
            qual = st.selectbox(T['quality'], ["320kbps (Gốc)", "256kbps", "192kbps", "128kbps"])
        else:
            # Nếu là Video -> Hiện độ phân giải (Dùng key 'best' an toàn)
            best_label = T.get('best', "Best (Auto)") 
            qual = st.selectbox(T['quality'], [best_label, "1080p", "720p", "480p"])

    with c_btn:
        # Class main-btn để CSS chỉnh màu
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        btn_dl = st.button(T['btn_dl'])
        st.markdown('</div>', unsafe_allow_html=True)

    # ➤ ADS DƯỚI NÚT TẢI
    # ĐÃ GẮN CODE QUẢNG CÁO SỐ 2 (300x250)
    components.html("""
    <div style="display:flex; justify-content:center; background:#111; height:250px; align-items:center; color:#555; border:1px dashed #333; margin-top:10px;">
        <script>
          atOptions = {
            'key' : 'fc08ecca6a7d3aa2086c08e8ee11a125',
            'format' : 'iframe',
            'height' : 250,
            'width' : 300,
            'params' : {}
          };
        </script>
        <script src="https://www.highperformanceformat.com/fc08ecca6a7d3aa2086c08e8ee11a125/invoke.js"></script>
    </div>
    """, height=260)

    # --- LOGIC DOWNLOAD ---
    if btn_dl:
        if not url:
            st.warning("⚠️ Link?")
        else:
            # ÉP XEM QUẢNG CÁO 3 GIÂY
            placeholder = st.empty()
            with placeholder.container():
                st.warning(T['wait'])
                components.html(f"""
                <div style="background:#000; color:gold; padding:20px; text-align:center; border:1px solid gold;">
                    <h2>{T['ad_wait']}</h2>
                </div>
                """, height=100)
                time.sleep(3)
            placeholder.empty()

            # TẢI THẬT
            try:
                ydl_opts = {
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'quiet': True,
                    'noplaylist': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                is_audio = (fmt == T['audio'])
                
                if is_audio:
                    # Lấy số bitrate (vd: "320")
                    bitrate = qual.split("k")[0]
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': bitrate,
                    }]
                else:
                    res_map = {"1080p": 1080, "720p": 720, "480p": 480}
                    if qual in res_map:
                        h = res_map[qual]
                        ydl_opts['format'] = f'bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}][ext=mp4]/best'
                    else:
                        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

                with st.spinner("Processing..."):
                    if not os.path.exists("downloads"): os.makedirs("downloads")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        f_path = ydl.prepare_filename(info)
                        if is_audio: 
                            base, _ = os.path.splitext(f_path)
                            f_path = base + ".mp3"

                if os.path.exists(f_path):
                    fname = os.path.basename(f_path)
                    st.success(T['success'])
                    with open(f_path, "rb") as f:
                        st.download_button(label=T['save_btn'], data=f, file_name=fname, mime="audio/mpeg" if is_audio else "video/mp4")
            except Exception as e:
                st.error(f"{T['error']} \nDetails: {str(e)}")

# ➤ CỘT PHẢI: ADS
# ĐÃ GẮN CODE QUẢNG CÁO SỐ 3 (160x600)
with col_R:
    components.html("""
    <div style="background:#111; height:600px; color:#555; display:flex; justify-content:center; align-items:center; border:1px dashed #444;">
        <script>
          atOptions = {
            'key' : 'a2290a3f17b278ebb0282ecbc8a7d5be',
            'format' : 'iframe',
            'height' : 600,
            'width' : 160,
            'params' : {}
          };
        </script>
        <script src="https://www.highperformanceformat.com/a2290a3f17b278ebb0282ecbc8a7d5be/invoke.js"></script>
    </div>
    """, height=600)

# --- 9. STICKY FOOTER ADS ---
# ĐÃ GẮN CODE QUẢNG CÁO SỐ 1 (728x90)
components.html("""
<div style="position:fixed; bottom:0; left:0; width:100%; background:#000; border-top:2px solid red; text-align:center; padding:10px; z-index:9999;">
    <script>
      atOptions = {
        'key' : '7cd087fd6ceed9ebc182a8dafcde705c',
        'format' : 'iframe',
        'height' : 90,
        'width' : 728,
        'params' : {}
      };
    </script>
    <script src="https://www.highperformanceformat.com/7cd087fd6ceed9ebc182a8dafcde705c/invoke.js"></script>
</div>
""", height=120)

# --- 10. POPUNDER / INVISIBLE ADS ---
# ĐÃ GẮN CODE QUẢNG CÁO SỐ 4 (Script chạy ngầm)
components.html("""
    <script src="https://pl28512831.effectivegatecpm.com/de/98/23/de982324f79133ce2d436361b3a8fdf3.js"></script>
""", height=0)
