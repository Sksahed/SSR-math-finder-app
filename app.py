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

# ২. Custom CSS: অ্যানিমেটেড ব্যাকগ্রাউন্ড, হাইড 'Manage app' ও স্টাইলিং
custom_css = """
<style>
    /* 🚫 Streamlit এর 'Manage app', ফুটার ও হেডার মেনু পুরোপুরি হাইড করার কোড */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
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
        line-height: 1.7 !important;
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

# ৪. এআই কনফিগারেশন ও স্পিড অপটিমাইজেশন ক্যাশিং
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    MODEL_NAME = 'gemini-2.5-flash'
    model = genai.GenerativeModel(MODEL_NAME)

    pdf_files = glob.glob("*.pdf") + glob.glob("books/*.pdf")
    image_files = glob.glob("books/*.png") + glob.glob("books/*.jpg") + glob.glob("books/*.jpeg")

    st.sidebar.markdown("### 📚 ডাটাবেজে স্থায়ী বইসমূহ")
    if pdf_files or image_files:
        st.sidebar.success(f"✅ {len(pdf_files) + len(image_files)}টি ফাইল সার্ভারে প্রস্তুত আছে।")
        for p in pdf_files:
            st.sidebar.caption(f"📖 {os.path.basename(p)}")
    else:
        st.sidebar.warning("⚠️ গিটহাবে কোনো বইয়ের PDF যুক্ত করা হয়নি। দয়া করে GitHub-এ PDF ফাইল আপলোড করুন।")

    st.sidebar.markdown("---")
    st.sidebar.info("🔒 নিরাপত্তা: শুধুমাত্র ফাউন্ডার (SK Sahed) গিটহাব থেকে নতুন বই যুক্ত করতে বা পরিবর্তন করতে পারবেন।")

    # ⚡ স্পিড বাড়ানোর জাদুকরী ফাংশন: ফাইলগুলোকে গুগল ক্লাউডে ক্যাশ করে রাখবে
    @st.cache_resource(show_spinner=False)
    def prepare_book_files(pdf_paths, img_paths):
        cached_files = []
        for pdf in pdf_paths:
            uploaded = genai.upload_file(pdf)
            cached_files.append(uploaded)
        for img in img_paths:
            uploaded = genai.upload_file(img)
            cached_files.append(uploaded)
        return cached_files

    # মূল অংক খোঁজার অংশ
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

    # ৫. দুটি অ্যাকশন বাটন
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        btn_find_only = st.button("🔍 অংকটি কোথায় আছে খোঁজো")

    with btn_col2:
        btn_find_with_solution = st.button("📝 অংকটি উত্তর সহ খোঁজো")

    # 🎬 ক্লোই পার্কের (Chloe Park) স্পিড বুক রিডিং GIF সহ লোডিং প্যানেল
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

    # বাটন লজিক প্রসেসিং
    if btn_find_only or btn_find_with_solution:
        if not (pdf_files or image_files):
            st.error("⚠️ গিটহাবে কোনো বই পাওয়া যায়নি! আগে গিটহাবে বইয়ের PDF ফাইল আপলোড করুন।")
        elif not query_image:
            st.error("⚠️ যে অংকটি স্ক্যান করতে চান, তার ছবি আপলোড করুন!")
        else:
            # অ্যানিমেটেড লোডিং স্ক্রিন
            loader_placeholder = st.empty()
            with loader_placeholder:
                show_custom_loading()

            try:
                # ১. ক্যাশ করা ফাইল লোড করা (এটি সেকেন্ডের মধ্যে প্রসেস শেষ করবে)
                book_contents = prepare_book_files(pdf_files, image_files)

                # ২. প্রম্পট সিলেক্ট করা
                if btn_find_only:
                    prompt = """
                    তুমি একজন সুনিপুণ গণিত শিক্ষক ও এআই স্ক্যানার।
                    তোমাকে পাঠ্যবইয়ের পৃষ্ঠা এবং শেষে একটি খাতার ছবি দেওয়া হয়েছে।

                    ⚠️ নির্দেশনাসমূহ:
                    ১. খাতার ছবিটির উপর থেকে নিচ পর্যন্ত থাকা **সকল অংক চিহ্নিত করো** (১০টি বা তার বেশি থাকলেও)।
                    ২. প্রতিটি অংক বইয়ের কোথায় আছে তা বের করো:
                       - **🎯 হুবহু মিল:** যদি বইয়ের প্রশ্ন ও সংখ্যা হুবহু এক হয়।
                       - **🔄 টাইপ / ধারণাগত মিল:** যদি প্রশ্নের নিয়ম বা টাইপ এক কিন্তু সংখ্যা পরিবর্তিত।
                    
                    ৩. কোনো বিস্তারিত সমাধানের প্রয়োজন নেই। শুধু নিচের ফরম্যাটে তথ্য দাও:

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
                    তুমি একজন অত্যন্ত সুনিপুণ ও অভিজ্ঞ গণিত শিক্ষক।
                    তোমাকে পাঠ্যবই এবং শেষে ইউজারের আপলোড করা একটি খাতার ছবি দেওয়া হয়েছে।

                    ⚠️ মূল নির্দেশনাসমূহ:
                    ১. খাতার ছবিতে ১টি থেকে ১০টি বা তার বেশি যতগুলোই অংক থাকুক না কেন, **প্রতিটি অংককে পৃথকভাবে শনাক্ত করো**।
                    ২. প্রতিটি অংক বইয়ের কোথায় আছে (অধ্যায়, পৃষ্ঠা ও দাগ নম্বর) তা বের করো।
                    ৩. 🎯 **বিশেষ প্রাধান্য (ধাপে ধাপে সমাধান):** প্রতিটি অংকের জন্য বইটিতে যে নিয়ম ও সূত্র ব্যবহার করা হয়েছে, ঠিক সেই নিয়ম মেনে **একদম পরিষ্কার ও ধাপে ধাপে (Step-by-Step)** কষে সমাধান প্রদান করো।
                       - কোনো শর্টকাট বা সরাসরি উত্তর দেওয়া যাবে না। 
                       - প্রতি লাইনে কীভাবে অংকটি এগোচ্ছে তা ধাপে ধাপে (ধাপ ১, ধাপ ২, ধাপ ৩...) স্পষ্ট করে বুঝিয়ে দাও।

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
                      * **ধাপ ১:** [প্রথম ধাপের গাণিতিক হিসেব ও ব্যাখ্যা]
                      * **ধাপ ২:** [দ্বিতীয় ধাপের গাণিতিক হিসেব ও ব্যাখ্যা]
                      * **ধাপ ৩:** [পরবর্তী ধাপের গাণিতিক হিসেব...]
                    - ✅ **চূড়ান্ত উত্তর (Final Answer):**
                    ---
                    (ছবিতে থাকা প্রতিটি অংকের জন্য ধাপে ধাপে বিস্তারিত সমাধান লেখো)
                    """

                # ৩. জেমিনির কাছে তথ্য পাঠানো (ক্যাশ করা ফাইল ব্যবহারে অতি দ্রুত কাজ করবে)
                contents = [prompt] + book_contents + ["\n[ইউজারের আপলোড করা খাতার ছবি]:", Image.open(query_image)]

                response = model.generate_content(contents)

                # লোডার রিমুভ করা
                loader_placeholder.empty()

                # রেজাল্ট প্রদর্শন
                st.balloons()
                st.markdown("""
                <div class="card" style="border-left: 6px solid #10b981;">
                    <h2 style="color: #34d399; margin:0;">🎉 অংক অনুসন্ধান ও বিশ্লেষণ সফল হয়েছে!</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.info(response.text)

            except Exception as e:
                loader_placeholder.empty()
                st.error(f"একটি সমস্যা হয়েছে: {e}")

except Exception as e:
    st.error("⚠️ অ্যাপ কনফিগারেশনে সমস্যা হয়েছে। দয়া করে Streamlit Secrets-এ সঠিক 'GEMINI_API_KEY' যুক্ত করুন।")
        
