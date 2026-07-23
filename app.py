import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজের লেআউট ও নাম সেটআপ
st.set_page_config(
    page_title="Math Finder AI Pro", 
    page_icon="⚡", 
    layout="wide"
)

# ২. Custom CSS: কালার, অ্যানিমেশন ও কার্টুন থিম
custom_css = """
<style>
    /* ব্যাকগ্রাউন্ড গ্রেডিয়েন্ট */
    .stApp {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        font-family: 'Comic Sans MS', 'Segoe UI', sans-serif;
    }

    /* হেডার বক্স স্টাইল */
    .header-container {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }

    /* প্রধান কার্ডের ডিজাইন */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        border: 3px solid #6c5ce7;
        margin-bottom: 20px;
    }

    /* সাইডবার সুন্দর করা */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }

    /* বাটনের রঙিন অ্যানিমেটেড লুক */
    .stButton > button {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(255, 75, 43, 0.4) !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 👑 AUTOMATIC POP-UP DIALOG WITH NORMAL PHOTO & ANIMATED STICKER ---
@st.dialog("👑 Meet the Founder")
def show_founder_popup():
    col1, col2 = st.columns([1, 2])
    with col1:
        founder_photo = "https://raw.githubusercontent.com/Sksahed/SSR-math-finder-app/refs/heads/main/IMG_20260609_112752_911.webp"
        
        # নরমাল ছবি এবং ছবিতে পিকাচু অ্যানিমেটেড স্টিকার
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="background: linear-gradient(45deg, #FF416C, #FF4B2B); color: white; padding: 5px 14px; border-radius: 20px; font-weight: bold; font-size: 12px; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">👑 FOUNDER</span>
            <br><br>
            <div style="position: relative; display: inline-block;">
                <!-- আসল শেপে নরমাল ছবি -->
                <img src="{founder_photo}" width="160" style="border-radius: 16px; border: 3px solid #6c5ce7; box-shadow: 0 6px 15px rgba(0,0,0,0.2);">
                <!-- ছবির ডান কোনে অ্যানিমেটেড পিকাচু -->
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif" width="50" style="position: absolute; bottom: -12px; right: -15px; filter: drop-shadow(0px 3px 5px rgba(0,0,0,0.3));">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<h2 style='color:#6c5ce7; margin:0;'>SK Sahed</h2>", unsafe_allow_html=True)
        st.markdown("<b style='color:#333;'>Lead Developer & Creator</b>", unsafe_allow_html=True)
        st.write("🚀 শিক্ষার্থীদের জন্য গণিত শেখা সহজ করতে এই AI প্ল্যাটফর্মটি তৈরি করা হয়েছে।")
    
    st.info("💡 'যেকোনো কঠিন অংক এখন এক ক্লিকে খুঁজে বের করো সহজে!'")
    st.success("স্বাগতম আমাদের Math Finder AI Pro প্ল্যাটফর্মে! 🌟")

# সাইটে ঢোকার সাথে সাথে অটোমেটিক পপ-আপ ওপেন করার লজিক
if "founder_popup_shown" not in st.session_state:
    st.session_state.founder_popup_shown = True
    show_founder_popup()

# ৩. অ্যানিমেটেড হেডার উইথ পিকাচু ও ডোরেমন
col_dora, col_head, col_pika = st.columns([1, 3, 1])

with col_dora:
    # ডোরেমন অ্যানিমেশন GIF
    st.image("https://media.giphy.com/media/l41FJv_sYvEw4P73y/giphy.gif", width=120)

with col_head:
    st.markdown("""
    <div class="header-container">
        <h1 style='margin:0;'>✨ Math Finder AI Pro ✨</h1>
        <p style='font-size: 16px; opacity: 0.95; margin-top: 8px;'>
            ডোরেমন ও পিকাচুর সাথে জাদুকরী এআই দিয়ে অংক খুঁজে বের করো!
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_pika:
    # পিকাচু অ্যানিমেশন GIF
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif", width=110)

# ৪. সাইডবার কনফিগারেশন
st.sidebar.markdown("### ⚙️ কনফিগারেশন")
api_key = st.sidebar.text_input("🔑 Gemini API Key দিন:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        MODEL_NAME = 'gemini-3.5-flash-lite'
        model = genai.GenerativeModel(MODEL_NAME)

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📚 ১. বই বা নোটস আপলোড")
        uploaded_book_pages = st.sidebar.file_uploader(
            "বইয়ের পৃষ্ঠা বা PDF ফাইল দিন:", 
            type=["png", "jpg", "jpeg", "pdf"], 
            accept_multiple_files=True
        )

        # মূল অংক খোঁজার অংশ
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown("""
            <div class="card">
                <h3>🔍 ২. নির্দিষ্ট অংক স্ক্যান করুন</h3>
                <p style='color: #555;'>বইতে খুঁজে না পাওয়া অংকটির ছবি নিচে আপলোড করে দাও।</p>
            </div>
            """, unsafe_allow_html=True)

            query_image = st.file_uploader(
                "অংকের ছবি সিলেক্ট করুন:", 
                type=["png", "jpg", "jpeg"]
            )
        
        with col_m2:
            st.image("https://media.giphy.com/media/1d5Zn8FNHJCMw/giphy.gif", width=130)

        st.markdown("<br>", unsafe_allow_html=True)

        # সার্চ বাটন
        if st.button("🚀 অংকটি ম্যাপিং ও সার্চ করো"):
            if not uploaded_book_pages:
                st.error("⚠️ দয়া করে আগে সাইডবার থেকে বইয়ের পৃষ্ঠা বা PDF ফাইল আপলোড করুন!")
            elif not query_image:
                st.error("⚠️ যে অংকটি বের করতে চান, তার ছবি আপলোড করুন!")
            else:
                with st.spinner("✨ জাদুকরী এআই দিয়ে বইয়ের পৃষ্ঠা স্ক্যান করা হচ্ছে..."):
                    try:
                        prompt = """
                        তুমি একজন অত্যন্ত দক্ষ গণিত শিক্ষক। 
                        তোমাকে নিচে কিছু বইয়ের পৃষ্ঠা/PDF এবং শেষে একটি নির্দিষ্ট অংকের ছবি দেওয়া হয়েছে।
                        
                        তোমার কাজ হলো:
                        ১. অংকটি বইয়ের কোনো পৃষ্ঠার সাথে মিলে যায় কিনা তা নিখুঁতভাবে চেক করা।
                        ২. উত্তরটি খুব সুন্দর ও স্পষ্ট বাংলায় উপস্থাপন করা:
                           - 📖 **অধ্যায় / লেসন:** 
                           - 📄 **পৃষ্ঠা নম্বর:** 
                           - 🔢 **অংক নম্বর:** 
                           - 💡 **সংক্ষিপ্ত সমাধান / ইঙ্গিত:**
                        
                        যদি হুবহু না পাওয়া যায়, তবে সবচেয়ে কাছাকাছি মিল থাকা অংকটির বিবরণ দাও।
                        """

                        contents = [prompt]

                        for index, page in enumerate(uploaded_book_pages):
                            contents.append(f"\n[বইয়ের পেজ {index + 1}]:")
                            if page.type == "application/pdf":
                                contents.append({"mime_type": "application/pdf", "data": page.getvalue()})
                            else:
                                contents.append(Image.open(page))

                        contents.append("\n[খুঁজতে চাওয়া অংক]:")
                        contents.append(Image.open(query_image))

                        response = model.generate_content(contents)

                        # সেলিব্রেশন ও ফলাফল
                        st.balloons()
                        st.markdown("""
                        <div class="card" style="border-left: 6px solid #28a745;">
                            <h2 style="color: #28a745;">🎉 ফলাফল পাওয়া গেছে!</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info(response.text)

                    except Exception as e:
                        st.error(f"একটি সমস্যা হয়েছে: {e}")

    except Exception as e:
        st.sidebar.error(f"API Key সেটআপে সমস্যা হয়েছে: {e}")
else:
    st.warning("👈 শুরু করতে বামপাশের সাইডবারে আপনার **Gemini API Key** বসান।")
        
