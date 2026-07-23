import streamlit as st
import requests
import base64
import os
import glob
from PIL import Image

# 🎯 তোমার পছন্দের সবচেয়ে ফাস্ট ও লাইট (Lite) মডেল নাম এখানে সেট করা হয়েছে:
# (ভবিষ্যতে গুগল নতুন কোনো মডেল আনলে তুমি শুধু এই নামটা বদলে নিতে পারবে)
MODEL_NAME = "gemini-3.5-flash-lite"

# ১. পেজের লেআউট ও নাম সেটআপ
st.set_page_config(
    page_title="Math Finder AI Pro", 
    page_icon="⚡", 
    layout="wide"
)

# ২. Custom CSS: অ্যানিমেটেড ব্যাকগ্রাউন্ড, স্টাইলিং ও টুলবার হাইড
custom_css = """
<style>
    /* 🚫 Streamlit এর 'Manage app', ফুটার ও হেডার মেনু পুরোপুরি হাইড করার কোড */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppToolbar {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    button[title="View app in Streamlit Community Cloud"] {display: none !important;}

    /* স্মুথ অ্যানিমেটেড ব্যাকগ্রাউন্ড গ্রেডিয়েন্ট */
    @keyframes animatedBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #4c1d95, #1e1b4b);
        background-size: 400% 400%;
        animation: animatedBackground 12s ease infinite;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        color: #f8fafc;
    }

    /* হেডার বক্স স্টাইল */
    .header-container {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        padding: 30px;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* স্টাইলিশ গ্লাসমরফিজম কার্ড */
    .card {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 24px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 20px;
    }

    /* সাইডবার স্টাইলিশ করা */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc;
    }

    /* আকর্ষণীয় রঙিন অ্যানিমেটেড বাটন */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        padding: 14px 20px !important;
        border-radius: 35px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.5) !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(236, 72, 153, 0.7) !important;
    }

    /* রেজাল্ট বক্সের (st.info / st.success) টেক্সট স্টাইল */
    [data-testid="stAlert"] {
        background: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(16px) !important;
        border: 2px solid #a855f7 !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        padding: 20px !important;
    }

    [data-testid="stAlert"] p, 
    [data-testid="stAlert"] li, 
    [data-testid="stAlert"] span, 
    [data-testid="stAlert"] div {
        color: #f1f5f9 !important;
        font-size: 16px !important;
        line-height: 1.7 !important;
    }

    [data-testid="stAlert"] strong {
        color: #38bdf8 !important;
        font-size: 17px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 👑 FOUNDER POPUP DIALOG ---
@st.dialog("👑 Meet the Founder")
def show_founder_popup():
    col1, col2 = st.columns([1, 2])
    with col1:
        founder_photo = "https://raw.githubusercontent.com/Sksahed/SSR-math-finder-app/refs/heads/main/IMG_20260609_112752_911.webp"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="background: linear-gradient(45deg, #ec4899, #8b5cf6); color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 12px; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">👑 FOUNDER</span>
            <br><br>
            <div style="position: relative; display: inline-block;">
                <img src="{founder_photo}" width="160" style="border-radius: 20px; border: 3px solid #a855f7; box-shadow: 0 8px 25px rgba(0,0,0,0.4);">
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif" width="50" style="position: absolute; bottom: -12px; right: -15px; filter: drop-shadow(0px 3px 5px rgba(0,0,0,0.5));">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<h2 style='color:#f43f5e; margin:0;'>SK Sahed</h2>", unsafe_allow_html=True)
        st.markdown("<b style='color:#cbd5e1;'>Lead Developer & Creator</b>", unsafe_allow_html=True)
        st.write("🚀 শিক্ষার্থীদের জন্য গণিত শেখা সহজ করতে এই AI প্ল্যাটফর্মটি তৈরি করা হয়েছে।")
    
    st.info("💡 'যেকোনো কঠিন অংক এখন এক ক্লিকে খুঁজে বের করো সহজে!'")
    st.success("স্বাগতম আমাদের Math Finder AI Pro প্ল্যাটফর্মে! 🌟")

if "founder_popup_shown" not in st.session_state:
    st.session_state.founder_popup_shown = True
    show_founder_popup()

# --- 🌟 TOP WELCOME BAR ---
founder_photo_url = "https://raw.githubusercontent.com/Sksahed/SSR-math-finder-app/refs/heads/main/IMG_20260609_112752_911.webp"

st.markdown(f"""
<div style="
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(12px);
    padding: 12px 20px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
">
    <img src="{founder_photo_url}" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 2px solid #a855f7;">
    <div>
        <div style="margin: 0; color: #f8fafc; font-size: 16px; font-weight: 600;">
            Welcome to my AI finding website 👋
        </div>
        <div style="margin: 0; font-size: 12px; color: #cbd5e1; font-weight: 500;">
            Created by SK Sahed
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ৩. Header
col_dora, col_head, col_pika = st.columns([1, 3, 1])

with col_dora:
    st.image("https://media.giphy.com/media/l41FJv_sYvEw4P73y/giphy.gif", width=100)

with col_head:
    st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>✨ Math Finder AI Pro ✨</h1>
        <p style='font-size: 16px; opacity: 0.95; margin-top: 8px;'>
            ডোরেমন ও পিকাচুর সাথে জাদুকরী এআই দিয়ে অংক খুঁজে বের করো!
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_pika:
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif", width=100)

# ৪. এপিআই কি ও ফাইলসমূহ চেক
try:
    raw_api_key = st.secrets["GEMINI_API_KEY"]
    api_key = str(raw_api_key).strip()

    pdf_files = glob.glob("*.pdf") + glob.glob("books/*.pdf")
    image_files = glob.glob("books/*.png") + glob.glob("books/*.jpg") + glob.glob("books/*.jpeg")

    st.sidebar.markdown("### 📚 ডাটাবেজে স্থায়ী বইসমূহ")
    if pdf_files or image_files:
        st.sidebar.success(f"✅ {len(pdf_files) + len(image_files)}টি ফাইল সার্ভারে প্রস্তুত আছে।")
        for p in pdf_files:
            st.sidebar.caption(f"📖 {os.path.basename(p)}")
    else:
        st.sidebar.warning("⚠️ গিটহাবে কোনো বইয়ের PDF যুক্ত করা হয়নি।")

    st.sidebar.markdown("---")
    st.sidebar.info("🔒 নিরাপত্তা: শুধুমাত্র ফাউন্ডার (SK Sahed) নতুন বই যুক্ত করতে পারবেন।")

    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        st.markdown("""
        <div class="card">
            <h3 style='color: #f8fafc; margin-top: 0;'>🔍 খাতার প্রশ্ন আপলোড করো</h3>
            <p style='color: #cbd5e1;'>খাতার পাতা বা অংকের ছবি আপলোড করো। এরপর নিচের যেকোনো একটি অপশনে ক্লিক করে স্ক্যান শুরু করো!</p>
        </div>
        """, unsafe_allow_html=True)

        query_image = st.file_uploader(
            "অংকের ছবি বা খাতার পৃষ্ঠা আপলোড করুন:", 
            type=["png", "jpg", "jpeg"]
        )
    
    with col_m2:
        st.image("https://media.giphy.com/media/1d5Zn8FNHJCMw/giphy.gif", width=120)

    st.markdown("<br>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        btn_find_only = st.button("🔍 অংকটি কোথায় আছে খোঁজো")

    with btn_col2:
        btn_find_with_solution = st.button("📝 অংকটি উত্তর সহ খোঁজো")

    # 🎬 ক্লোই পার্কের (Chloe Park) দ্রুত বই পড়ার GIF সহ লোডার
    def show_custom_loading():
        return st.markdown("""
        <div style="
            background: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(16px);
            padding: 20px;
            border-radius: 24px;
            border: 2px solid #a855f7;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        ">
            <img src="https://media.giphy.com/media/l0HlTy9x8FZo0XO1i/giphy.gif" width="110" style="border-radius: 16px; border: 2px solid #ec4899; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));">
            <div style="text-align: left;">
                <h4 style="color: #f8fafc; margin: 0; font-size: 18px; font-weight: 600; line-height: 1.4;">
                    একটু wait করুন Sk sahed স্যার পিকাচু আর ডোরেমন কে সাথে নিয়ে আপনার প্রশ্নটি খুঁজছে... 🔍⚡
                </h4>
                <p style="color: #38bdf8; margin: 6px 0 0 0; font-size: 13px; font-weight: 500;">
                    📖 বইয়ের সকল অধ্যায় ও পৃষ্ঠা স্ক্যান করা হচ্ছে...
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ⚡ গুগল REST API (Flash-Lite / Light-weight মডেল ব্যবহার করে)
    def call_gemini_api(api_key, prompt_text, pdf_paths, image_paths, user_img_file):
        parts = [{"text": prompt_text}]

        # ১. বইয়ের PDF যুক্ত করা
        for pdf_path in pdf_paths:
            with open(pdf_path, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_b64
                    }
                })

        # ২. বইয়ের ছবিসমূহ যুক্ত করা
        for img_path in image_paths:
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                mime = "image/png" if img_path.lower().endswith(".png") else "image/jpeg"
                parts.append({
                    "inline_data": {
                        "mime_type": mime,
                        "data": img_b64
                    }
                })

        # ৩. ইউজারের আপলোড করা খাতার ছবি যুক্ত করা
        user_img_bytes = user_img_file.getvalue()
        user_img_b64 = base64.b64encode(user_img_bytes).decode('utf-8')
        mime_type = user_img_file.type if user_img_file.type else "image/jpeg"
        
        parts.append({"text": "\n[ইউজারের আপলোড করা খাতার ছবি]:"})
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": user_img_b64
            }
        })

        payload = {
            "contents": [{
                "parts": parts
            }]
        }

        # 🚀 নির্ধারিত মডেলের REST API এন্ডপয়েন্ট
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers, timeout=120)
        res_data = response.json()

        if response.status_code == 200:
            try:
                return res_data['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                return "দুঃখিত, কোনো উত্তর পাওয়া যায়নি।"
        else:
            error_msg = res_data.get('error', {}).get('message', 'অজানা এরর')
            raise Exception(f"গুগল এপিআই এরর (Code {response.status_code}): {error_msg}")

    if btn_find_only or btn_find_with_solution:
        if not (pdf_files or image_files):
            st.error("⚠️ গিটহাবে কোনো বই পাওয়া যায়নি! আগে গিটহাবে বইয়ের PDF ফাইল আপলোড করুন।")
        elif not query_image:
            st.error("⚠️ যে অংকটি স্ক্যান করতে চান, তার ছবি আপলোড করুন!")
        else:
            loader_placeholder = st.empty()
            with loader_placeholder:
                show_custom_loading()

            try:
                if btn_find_only:
                    prompt = """
                    তুমি একজন সুনিপুণ গণিত শিক্ষক ও এআই স্ক্যানার।
                    তোমাকে পাঠ্যবইয়ের PDF পৃষ্ঠা এবং শেষে খাতার ছবি দেওয়া হয়েছে।

                    ⚠️ নির্দেশনাসমূহ:
                    ১. খাতার ছবিটিতে থাকা **সকল অংক চিহ্নিত করো**।
                    ২. প্রতিটি অংক বইয়ের কোথায় আছে তা বের করো:
                       - **🎯 হুবহু মিল:** যদি বইয়ের প্রশ্ন ও সংখ্যা হুবহু এক হয়।
                       - **🔄 টাইপ / ধারণাগত মিল:** যদি প্রশ্নের নিয়ম এক কিন্তু সংখ্যা পরিবর্তিত।
                    
                    ৩. নিম্নের বিন্যাসে তথ্য উপস্থাপন করো:

                    ---
                    ### 🔢 অংক ১: [খাতায় থাকা অংকটি]
                    - 📌 **স্ট্যাটাস:** (🎯 হুবহু মিল / 🔄 টাইপ মিল)
                    - 📖 **অধ্যায় / পাঠ্যবিষয়:** 
                    - 📄 **বইয়ের পৃষ্ঠা নম্বর:** 
                    - 🔢 **বইয়ের কোশ্চেন/দাগ নম্বর:** 
                    - 💡 **সংক্ষিপ্ত সূত্র/ধরন:**
                    ---
                    (ছবিতে থাকা প্রতিটি অংকের জন্য একইভাবে তথ্য দাও)
                    """
                else:
                    prompt = """
                    তুমি একজন অভিজ্ঞ গণিত শিক্ষক।
                    তোমাকে পাঠ্যবই এবং শেষে ইউজারের খাতার ছবি দেওয়া হয়েছে।

                    ⚠️ মূল নির্দেশনাসমূহ:
                    ১. খাতার ছবিটির প্রতিটি অংক পৃথকভাবে শনাক্ত করো।
                    ২. প্রতিটি অংক বইয়ের কোথায় আছে (অধ্যায়, পৃষ্ঠা ও দাগ নম্বর) বের করো।
                    ৩. 🎯 **ধাপে ধাপে সমাধান:** বইয়ের নির্দিষ্ট নিয়ম ও সূত্র প্রয়োগ করে অংকগুলোর **ধাপে ধাপে (Step 1, Step 2, Step 3...) সম্পূর্ণ সমাধান** লেখো।

                    ৪. আউটপুট ফরম্যাট:

                    ---
                    ### 🔢 অংক ১: [খাতায় থাকা প্রশ্নটি]
                    - 📌 **ম্যাচিং স্ট্যাটাস:** (🎯 হুবহু মিল / 🔄 টাইপ বা ধরন মিল)
                    - 📖 **অধ্যায়:** 
                    - 📄 **বইয়ের পৃষ্ঠা নম্বর:** 
                    - 🔢 **বইয়ের কোশ্চেন/দাগ নম্বর:** 

                    #### 📝 বইয়ের নিয়মে ধাপে ধাপে সম্পূর্ণ সমাধান:
                    - 📐 **প্রযোজ্য সূত্র / নিয়ম:**
                    - ✍️ **ধাপে ধাপে সমাধান (Step-by-Step):**
                      * **ধাপ ১:** [প্রথম ধাপের হিসেব ও ব্যাখ্যা]
                      * **ধাপ ২:** [দ্বিতীয় ধাপের হিসেব ও ব্যাখ্যা]
                      * **ধাপ ৩:** [পরবর্তী ধাপ...]
                    - ✅ **চূড়ান্ত উত্তর (Final Answer):**
                    ---
                    (ছবিতে থাকা প্রতিটি অংকের জন্য বিস্তারিত সমাধান লেখো)
                    """

                # এপিআই কল
                result_text = call_gemini_api(api_key, prompt, pdf_files, image_files, query_image)

                loader_placeholder.empty()

                st.balloons()
                st.markdown("""
                <div class="card" style="border-left: 6px solid #10b981;">
                    <h2 style="color: #34d399; margin:0;">🎉 অংক অনুসন্ধান ও বিশ্লেষণ সফল হয়েছে!</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.info(result_text)

            except Exception as e:
                loader_placeholder.empty()
                st.error(f"একটি সমস্যা হয়েছে: {e}")

except Exception as e:
    st.error("⚠️ অ্যাপ কনফিগারেশনে সমস্যা হয়েছে। Streamlit Secrets-এ 'GEMINI_API_KEY' সঠিক আছে কিনা নিশ্চিত করুন।")
        
