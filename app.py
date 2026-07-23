import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import glob

# ১. পেজের লেআউট ও নাম সেটআপ
st.set_page_config(
    page_title="Math Finder AI Pro", 
    page_icon="⚡", 
    layout="wide"
)

# ২. Custom CSS: আকর্ষণীয় অ্যানিমেটেড ব্যাকগ্রাউন্ড ও হাই-কন্ট্রাস্ট টেক্সট থিম
custom_css = """
<style>
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
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 14px 30px !important;
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

    /* রেজাল্ট বক্সের (st.info / st.success) টেক্সট পরিষ্কার ও উজ্জ্বল করার নিয়ম */
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
        line-height: 1.6 !important;
    }

    [data-testid="stAlert"] strong {
        color: #38bdf8 !important;
        font-size: 17px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 👑 AUTOMATIC POP-UP DIALOG WITH YOUR PHOTO & PIKACHU ---
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

# সাইটে ঢোকার সাথে সাথে অটোমেটিক পপ-আপ ওপেন করার লজিক
if "founder_popup_shown" not in st.session_state:
    st.session_state.founder_popup_shown = True
    show_founder_popup()

# --- 🌟 ওপরে স্টাইলিশ ওয়েলকাম বার ---
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

# ৩. অ্যানিমেটেড হেডার উইথ পিকাচু ও ডোরেমন
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

# ৪. অটোমেটিক জেমিনি এআই কনফিগারেশন ও অটো-বই লোডার
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    MODEL_NAME = 'gemini-3.5-flash-lite'
    model = genai.GenerativeModel(MODEL_NAME)

    # গিটহাব ডিরেক্টরি থেকে স্বয়ংক্রিয়ভাবে সব PDF ও ছবি লোড করা
    pdf_files = glob.glob("*.pdf") + glob.glob("books/*.pdf")
    image_files = glob.glob("books/*.png") + glob.glob("books/*.jpg") + glob.glob("books/*.jpeg")

    st.sidebar.markdown("### 📚 ডাটাবেজে স্থায়ী বইসমূহ")
    if pdf_files or image_files:
        st.sidebar.success(f"✅ {len(pdf_files) + len(image_files)}টি ফাইল সার্ভারে স্থায়ীভাবে সংরক্ষিত আছে।")
        for p in pdf_files:
            st.sidebar.caption(f"📖 {os.path.basename(p)}")
    else:
        st.sidebar.warning("⚠️ গিটহাবে কোনো বইয়ের PDF যুক্ত করা হয়নি। দয়া করে GitHub-এ PDF ফাইল আপলোড করুন।")

    st.sidebar.markdown("---")
    st.sidebar.info("🔒 নিরাপত্তা: শুধুমাত্র ফাউন্ডার (SK Sahed) গিটহাব থেকে নতুন বই যুক্ত করতে বা পরিবর্তন করতে পারবেন।")

    # মূল অংক খোঁজার অংশ
    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        st.markdown("""
        <div class="card">
            <h3 style='color: #f8fafc; margin-top: 0;'>🔍 খাতার মাল্টিপল (১০+) অংক ও প্যাটার্ন স্ক্যানার</h3>
            <p style='color: #cbd5e1;'>খাতার পাতায় ১টি থেকে শুরু করে ১০ বা তার বেশি যতগুলোই অংক থাকুক, এআই উপর থেকে নিচে সবগুলো স্ক্যান করে টাইপ ও সূত্র অনুযায়ী ম্যাচ করাবে!</p>
        </div>
        """, unsafe_allow_html=True)

        query_image = st.file_uploader(
            "অংকের ছবি বা খাতার সম্পূর্ণ পৃষ্ঠা আপলোড করুন:", 
            type=["png", "jpg", "jpeg"]
        )
    
    with col_m2:
        st.image("https://media.giphy.com/media/1d5Zn8FNHJCMw/giphy.gif", width=120)

    st.markdown("<br>", unsafe_allow_html=True)

    # সার্চ বাটন
    if st.button("🚀 সকল (১০+) অংক ও প্যাটার্ন স্ক্যান করো"):
        if not (pdf_files or image_files):
            st.error("⚠️ গিটহাবে কোনো বই পাওয়া যায়নি! আগে গিটহাবে বইয়ের PDF ফাইল আপলোড করুন।")
        elif not query_image:
            st.error("⚠️ যে খাতা/পৃষ্ঠাটি স্ক্যান করতে চান, তার ছবি আপলোড করুন!")
        else:
            with st.spinner("✨ খাতার পাতায় থাকা ১০+ অংক ও বইয়ের গাণিতিক টাইপ স্ক্যান করা হচ্ছে..."):
                try:
                    # 🎯 ১০+ অংক নিখুঁতভাবে স্ক্যান করার জন্য আপগ্রেডেড প্রম্পট
                    prompt = """
                    তুমি একজন অত্যন্ত সূক্ষ্মদৃষ্টিসম্পন্ন গণিত শিক্ষক ও এআই স্ক্যানার।
                    তোমাকে সংরক্ষিত বইয়ের PDF/পৃষ্ঠা এবং শেষে একটি খাতার ছবি দেওয়া হয়েছে।

                    ⚠️ বিশেষ নির্দেশনা:
                    ১. খাতার ছবিটির একদম উপর থেকে নিচ পর্যন্ত ক্রমানুসারে (১, ২, ৩ ... ১০+) থাকা **সবকটি অংক চিহ্নিত করো**। ছবিতে যদি ১০টি বা তার বেশি অংক থাকে, তবে কোনো অংককেই এড়িয়ে যাওয়া যাবে না।
                    ২. প্রতিটি অংকের ক্ষেত্রে বইয়ের সাথে ২ ভাবে মিল খোঁজো:
                       - **🎯 হুবহু মিল:** প্রশ্ন ও সংখ্যা উভয়ই যদি বইয়ের সাথে মিলে যায়।
                       - **🔄 টাইপ / ধারণাগত মিল:** যদি প্রশ্নের নিয়ম/টাইপ সেম থাকে কিন্তু সংখ্যা বা প্রতীক পরিবর্তিত থাকে।

                    ৩. সংক্ষিপ্ত ও পরিচ্ছন্নভাবে প্রতিটির বিবরণ দাও:

                    ---
                    ### 🔢 অংক ১: [খাতায় থাকা অংকটি]
                    - 📌 **স্ট্যাটাস:** (🎯 হুবহু মিল / 🔄 টাইপ মিল)
                    - 📖 **অধ্যায় ও পৃষ্ঠা:** 
                    - 🔢 **বইয়ের অনুরূপ নম্বর:** 
                    - 💡 **সংক্ষিপ্ত নিয়ম/সূত্র:**

                    ---
                    ### 🔢 অংক ২: [খাতায় থাকা অংকটি]
                    - 📌 **স্ট্যাটাস:** ...
                    (খাতার ছবিতে থাকা বাকি অংকগুলো একইভাবে ১, ২, ৩, ৪, ৫, ৬, ৭, ৮, ৯, ১০+ পর্যন্ত বিস্তারিত সাজাও)
                    """

                    contents = [prompt]

                    # ১. গিটহাবে জমা থাকা PDF ফাইলগুলো প্রসেস করা
                    for pdf_path in pdf_files:
                        with open(pdf_path, "rb") as f:
                            contents.append({"mime_type": "application/pdf", "data": f.read()})

                    # ২. গিটহাবে জমা থাকা ছবি প্রসেস করা
                    for img_path in image_files:
                        contents.append(Image.open(img_path))

                    # ৩. ইউজারের আপলোড করা খাতার ছবি যুক্ত করা
                    contents.append("\n[ইউজারের আপলোড করা খাতার ছবি]:")
                    contents.append(Image.open(query_image))

                    response = model.generate_content(contents)

                    st.balloons()
                    st.markdown("""
                    <div class="card" style="border-left: 6px solid #10b981;">
                        <h2 style="color: #34d399; margin:0;">🎉 ১০+ অংকের অল-ইন-ওয়ান স্ক্যানিং সম্পূর্ণ!</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(response.text)

                except Exception as e:
                    st.error(f"একটি সমস্যা হয়েছে: {e}")

except Exception as e:
    st.error("⚠️ অ্যাপ কনফিগারেশনে সমস্যা হয়েছে। দয়া করে Streamlit Secrets-এ সঠিক 'GEMINI_API_KEY' যুক্ত করুন।")
        
