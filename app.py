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

# ২. Custom CSS: থিম ও ভিজ্যুয়াল স্টাইলিং
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

# ৪. সিকিউর এপিআই কনফিগারেশন
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("⚠️ Streamlit Secrets-এ GEMINI_API_KEY পাওয়া যায়নি! অনুগ্রহ করে Streamlit App Settings-এ গিয়ে এটি সেট করুন।")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 📚 টেক্সট ফাইল লোড
        txt_files = sorted([f for f in glob.glob("*.txt") if f.lower() != "requirements.txt"] + glob.glob("books/*.txt"))
        full_book_data = ""
        st.sidebar.markdown("### 📚 ডাটাবেজ স্ট্যাটাস")
        if txt_files:
            st.sidebar.success(f"✅ {len(txt_files)}টি টেক্সট ফাইল লোড করা হয়েছে।")
            for file in txt_files:
                st.sidebar.caption(f"📖 {os.path.basename(file)}")
                with open(file, "r", encoding="utf-8") as f:
                    full_book_data += f"\n\n=== [ ফাইল: {os.path.basename(file)} ] ===\n\n" + f.read()
        else:
            st.sidebar.warning("⚠️ গিটহাবে কোনো টেক্সট (.txt) ফাইল খুঁজে পাওয়া যায়নি।")

        st.sidebar.markdown("---")
        st.sidebar.info("🔒 নিরাপত্তা: শুধুমাত্র ফাউন্ডার (SK Sahed) নতুন ফাইল যুক্ত করতে পারবেন।")

        # 🔍 খাতার প্রশ্ন আপলোড
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown("""
            <div class="card" style="border-left: 6px solid #ec4899;">
                <h3 style='color: #f8fafc; margin-top: 0;'>🔍 খাতার প্রশ্ন আপলোড করো</h3>
                <p style='color: #cbd5e1; font-size: 14px;'>তোমার খাতার পাতা বা বইয়ের অংকের ছবি আপলোড করো। সম্পূর্ণ বইয়ের ডাটাবেজ থেকে এআই মুহূর্তেই সঠিক অংক ও উত্তর খুঁজে দেবে!</p>
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
                        ⚡ সম্পূর্ণ বইয়ের টেক্সট ডাটাবেজ থেকে দ্রুত স্ক্যান করা হচ্ছে...
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # সার্চ লজিক
        if btn_find_only or btn_find_with_solution:
            if not txt_files:
                st.error("⚠️ গিটহাবে কোনো বইয়ের টেক্সট (.txt) ফাইল নেই!")
            elif not query_image:
                st.error("⚠️ যে অংকটি স্ক্যান করতে চান, তার ছবি আপলোড করুন!")
            else:
                loader_placeholder = st.empty()
                with loader_placeholder:
                    show_custom_loading()

                try:
                    if btn_find_only:
                        prompt = f"""
                        তুমি একজন সুনিপুণ গণিত শিক্ষক ও এআই স্ক্যানার।
                        তোমাকে পাঠ্যবইয়ের সম্পূর্ণ টেক্সট ডাটাবেজ এবং নিচে একটি খাতার অংকের ছবি দেওয়া হয়েছে।

                        --- [ পাঠ্যবইয়ের ডাটাবেজ শুরু ] ---
                        {full_book_data}
                        --- [ পাঠ্যবইয়ের ডাটাবেজ শেষ ] ---

                        অংকটি বইয়ের মধ্যে খুঁজে নিয়ে অধ্যায়, পৃষ্ঠা ও দাগ নম্বর প্রদান করো।
                        """
                    else:
                        prompt = f"""
                        তুমি একজন অভিজ্ঞ গণিত শিক্ষক।
                        তোমাকে পাঠ্যবইয়ের সম্পূর্ণ টেক্সট ডাটাবেজ এবং নিচে একটি খাতার অংকের ছবি দেওয়া হয়েছে।

                        --- [ পাঠ্যবইয়ের ডাটাবেজ শুরু ] ---
                        {full_book_data}
                        --- [ পাঠ্যবইয়ের ডাটাবেজ শেষ ] ---

                        অংকটি কোথায় আছে তা বের করো এবং ধাপে ধাপে (Step-by-Step) সমাধান করো।
                        """

                    contents = [prompt, Image.open(query_image)]
                    response = model.generate_content(contents)

                    loader_placeholder.empty()
                    st.balloons()
                    
                    st.markdown("""
                    <div class="card" style="border-left: 6px solid #10b981;">
                        <h2 style="color: #34d399; margin:0;">🎉 অংক অনুসন্ধান সফল হয়েছে!</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(response.text)

                except Exception as e:
                    loader_placeholder.empty()
                    st.error(f"একটি সমস্যা হয়েছে: {e}")

except Exception as e:
    st.error(f"অ্যাপ কনফিগারেশনে সমস্যা: {e}")
        
