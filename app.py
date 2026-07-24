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

# ২. Custom CSS: স্টাইল ও থিম
custom_css = """
<style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppToolbar {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}

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

    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc;
    }

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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 👑 AUTOMATIC POP-UP DIALOG ---
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
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif" width="50" style="position: absolute; bottom: -12px; right: -15px;">
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
        <div style="margin: 0; color: #f8fafc; font-size: 16px; font-weight: 600;">Welcome to my AI finding website 👋</div>
        <div style="margin: 0; font-size: 12px; color: #cbd5e1; font-weight: 500;">Created by SK Sahed</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ৩. হেডার
col_dora, col_head, col_pika = st.columns([1, 3, 1])
with col_dora:
    st.image("https://media.giphy.com/media/l41FJv_sYvEw4P73y/giphy.gif", width=100)
with col_head:
    st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight: 700;'>✨ Math Finder AI Pro ✨</h1>
        <p style='font-size: 16px; opacity: 0.95; margin-top: 8px;'>ডোরেমন ও পিকাচুর সাথে জাদুকরী এআই দিয়ে অংক খুঁজে বের করো!</p>
    </div>
    """, unsafe_allow_html=True)
with col_pika:
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif", width=100)

# 📚 গিটহাব ডিরেক্টরি থেকে PDF ফাইল খোঁজার ফাংশন
def find_pdf_files():
    pdf_list = sorted(glob.glob("*.pdf") + glob.glob("*.PDF") + glob.glob("books/*.pdf") + glob.glob("books/*.PDF"))
    return pdf_list

# ৪. সিকিউর এপিআই কনফিগারেশন
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("⚠️ Streamlit Secrets-এ GEMINI_API_KEY পাওয়া যায়নি! অনুগ্রহ করে Streamlit App Settings-এ গিয়ে এটি সেট করুন।")
    else:
        genai.configure(api_key=api_key)

        pdf_files = find_pdf_files()
        
        st.sidebar.markdown("### 📚 পিডিএফ ডাটাবেজ স্ট্যাটাস")
        if pdf_files:
            st.sidebar.success(f"✅ {len(pdf_files)}টি পিডিএফ ফাইল সংযুক্ত আছে।")
            for pdf_path in pdf_files:
                st.sidebar.caption(f"📖 {os.path.basename(pdf_path)}")
        else:
            st.sidebar.warning("⚠️ গিটহাবে কোনো পিডিএফ (.pdf) ফাইল খুঁজে পাওয়া যায়নি।")

        st.sidebar.markdown("---")
        st.sidebar.info("🔒 নিরাপত্তা: শুধুমাত্র ফাউন্ডার (SK Sahed) নতুন ফাইল যুক্ত করতে পারবেন।")

        # 🔍 খাতার প্রশ্ন আপলোড
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown("""
            <div class="card" style="border-left: 6px solid #ec4899;">
                <h3 style='color: #f8fafc; margin-top: 0;'>🔍 খাতার প্রশ্ন আপলোড করো</h3>
                <p style='color: #cbd5e1; font-size: 14px;'>তোমার খাতার পাতা বা বইয়ের অংকের ছবি আপলোড করো। সম্পূর্ণ পিডিএফ বইয়ের ডাটাবেজ থেকে এআই মুহূর্তেই সঠিক অংক ও উত্তর খুঁজে দেবে!</p>
            </div>
            """, unsafe_allow_html=True)

            query_image = st.file_uploader(
                "অংকের ছবি বা খাতার পৃষ্ঠা আপলোড করুন:", 
                type=["png", "jpg", "jpeg"]
            )
        
        with col_m2:
            st.image("https://media.giphy.com/media/1d5Zn8FNHJCMw/giphy.gif", width=120)

        st.markdown("<br>", unsafe_allow_html=True)

        # অ্যাকশন বাটন
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            btn_find_only = st.button("🔍 অংকটি কোথায় আছে খোঁজো")
        with btn_col2:
            btn_find_with_solution = st.button("📝 অংকটি উত্তর সহ খোঁজো")

        # 🎬 কাস্টম GIF অ্যানিমেশন
        def show_custom_loading():
            gif_url = "https://raw.githubusercontent.com/Sksahed/SSR-math-finder-app/refs/heads/main/loading.gif"
            return st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.95); backdrop-filter: blur(16px); padding: 20px; border-radius: 24px; border: 2px solid #a855f7; display: flex; align-items: center; justify-content: center; gap: 20px; margin: 20px 0;">
                <img src="{gif_url}" width="140" style="border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
                <div>
                    <h4 style="color: #f8fafc; margin: 0; font-size: 18px; font-weight: 600;">
                        একটু wait করুন, দ্রুত বইয়ের পাতা উল্টে আপনার প্রশ্নটি খোঁজা হচ্ছে... 🔍📖
                    </h4>
                    <p style="color: #38bdf8; margin: 5px 0 0 0; font-size: 13px;">
                        ⚡ স্ক্যান করা পিডিএফ সরাসরি AI দিয়ে বিশ্লেষণ করা হচ্ছে...
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 🛡️ Gemini API-তে সরাসরি PDF ফাইল আপলোড ও প্রসেস করার সেফ ফাংশন
        def process_with_gemini(prompt, target_pdf_path, user_image_file):
            candidate_models = ['gemini-1.5-flash', 'gemini-2.0-flash-lite-preview-02-05', 'gemini-1.5-pro']
            
            # Gemini-র কাছে সরাসরি পুরো PDF আপলোড (যা ছবির মতো পড়া যায়)
            uploaded_pdf = genai.upload_file(target_pdf_path)
            
            last_error = None
            for m_name in candidate_models:
                try:
                    m = genai.GenerativeModel(m_name)
                    # প্রম্পট, পিডিএফ ফাইল এবং ইউজার ছবি একসাথে প্রসেস করা
                    response = m.generate_content([prompt, uploaded_pdf, Image.open(user_image_file)])
                    return response.text
                except Exception as err:
                    last_error = err
                    continue
            raise last_error

        # সার্চ লজিক
        if btn_find_only or btn_find_with_solution:
            if not pdf_files:
                st.error("⚠️ গিটহাবে কোনো পিডিএফ (.pdf) ফাইল নেই! দয়া করে গিটহাবে পিডিএফ ফাইল আপলোড রয়েছে কিনা নিশ্চিত করুন।")
            elif not query_image:
                st.error("⚠️ যে অংকটি স্ক্যান করতে চান, তার ছবি আপলোড করুন!")
            else:
                loader_placeholder = st.empty()
                with loader_placeholder:
                    show_custom_loading()

                try:
                    primary_pdf = pdf_files[0] # প্রধান পিডিএফ ফাইল বেছে নেয়া

                    if btn_find_only:
                        prompt = """
                        তুমি একজন অভিজ্ঞ গণিত শিক্ষক ও AI সার্চ এআই।
                        তোমাকে একটি পাঠ্যবইয়ের পুরো PDF এবং একটি খাতার অংকের ছবি দেওয়া হলো।

                        কী করবে:
                        ১. খাতার ছবির অংকটি PDF বইয়ের মধ্যে খুঁজে বের করো।
                        ২. বইয়ের কত নম্বর অধ্যায়, কত নম্বর পৃষ্ঠা (Page) এবং কত দাগ নম্বর অংকটি রয়েছে তা পরিষ্কার বাংলা ভাষায় সংক্ষেপে জানিয়ে দাও।
                        """
                    else:
                        prompt = """
                        তুমি একজন অভিজ্ঞ গণিত শিক্ষক।
                        তোমাকে একটি পাঠ্যবইয়ের পুরো PDF এবং একটি খাতার অংকের ছবি দেওয়া হলো।

                        কী করবে:
                        ১. খাতার ছবির অংকটি PDF বইয়ের কোথায় আছে তা খুঁজে বের করো (অধ্যায়, পৃষ্ঠা ও দাগ নম্বর)।
                        ২. অংকটি বইয়ের নিয়ম মেনে নিখুঁতভাবে ধাপে ধাপে (Step-by-Step) সহজ ভাষায় সমাধান করে দাও।
                        """

                    result_text = process_with_gemini(prompt, primary_pdf, query_image)

                    loader_placeholder.empty()
                    st.balloons()
                    
                    st.markdown("""
                    <div class="card" style="border-left: 6px solid #10b981;">
                        <h2 style="color: #34d399; margin:0;">🎉 অংক অনুসন্ধান সফল হয়েছে!</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(result_text)

                except Exception as e:
                    loader_placeholder.empty()
                    st.error(f"একটি সমস্যা হয়েছে: {e}")

except Exception as e:
    st.error(f"অ্যাপ কনফিগারেশনে সমস্যা: {e}")
        
