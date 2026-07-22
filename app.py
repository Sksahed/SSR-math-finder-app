import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজের লেআউট ও নাম সেটআপ
st.set_page_config(
    page_title="Math Finder AI Pro", 
    page_icon="🎓", 
    layout="wide"
)

# ২. Custom CSS: কালার, অ্যানিমেশন ও মডার্ন ডিজাইন
custom_css = """
<style>
    /* ব্যাকগ্রাউন্ড গ্রেডিয়েন্ট ও ফন্ট */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* হেডার বক্স স্টাইল ও ফেড-ইন অ্যানিমেশন */
    .header-container {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-bottom: 25px;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* প্রধান কার্ডের ডিজাইন */
    .card {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #4b6cb7;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
    }

    /* সাইডবার সুন্দর করা */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }

    /* বাটনের রঙিন অ্যানিমেটেড লুক */
    .stButton > button {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(221, 36, 118, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(221, 36, 118, 0.6) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ৩. অ্যানিমেটেড হেডার
st.markdown("""
<div class="header-container">
    <h1 style='margin:0;'>✨ Math Finder AI Pro ✨</h1>
    <p style='font-size: 16px; opacity: 0.9; margin-top: 8px;'>
        স্মার্ট এআই দিয়ে যেকোনো অংকের লেসন ও পৃষ্ঠা নম্বর খুঁজে বের করুন এক ক্লিকে!
    </p>
</div>
""", unsafe_allow_html=True)

# ৪. সাইডবার সেটআপ
st.sidebar.markdown("### ⚙️ কনফিগারেশন")
api_key = st.sidebar.text_input("🔑 Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # সঠিক মডেল নেম gemini-1.5-flash সেট করা হলো
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 ১. বই বা নোটস আপলোড")
    uploaded_book_pages = st.sidebar.file_uploader(
        "বইয়ের পৃষ্ঠা বা PDF ফাইল দিন:", 
        type=["png", "jpg", "jpeg", "pdf"], 
        accept_multiple_files=True
    )

    # ৫. প্রধান পেজের কন্টেন্ট
    st.markdown("""
    <div class="card">
        <h3>🔍 ২. নির্দিষ্ট অংক স্ক্যান করুন</h3>
        <p style='color: #666;'>আপনি যে অংকটি বইতে খুঁজে পাচ্ছেন না, সেটির ছবি নিচে আপলোড করুন।</p>
    </div>
    """, unsafe_allow_html=True)

    query_image = st.file_uploader(
        "অংকের ছবি সিলেক্ট করুন:", 
        type=["png", "jpg", "jpeg"]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # সার্চ বাটন
    if st.button("🚀 অংকটি ম্যাপিং ও সার্চ করো"):
        if not uploaded_book_pages:
            st.error("⚠️ দয়া করে আগে সাইডবার থেকে বইয়ের পৃষ্ঠা বা PDF ফাইল আপলোড করুন!")
        elif not query_image:
            st.error("⚠️ যে অংকটি বের করতে চান, তার ছবি আপলোড করুন!")
        else:
            with st.spinner("✨ AI আপনার বইয়ের সমস্ত পৃষ্ঠা স্ক্যান করে তথ্য ম্যাচ করছে..."):
                try:
                    prompt = """
                    তুমি একজন অত্যন্ত দক্ষ গণিত শিক্ষক ও গবেষক। 
                    তোমাকে নিচে কিছু বইয়ের পৃষ্ঠা/PDF এবং শেষে একটি নির্দিষ্ট অংকের ছবি দেওয়া হয়েছে।
                    
                    তোমার কাজ হলো:
                    ১. অংকটি বইয়ের কোনো পৃষ্ঠার সাথে মিলে যায় কিনা তা নিখুঁতভাবে চেক করা।
                    ২. উত্তরটি খুব সুন্দর, স্পষ্ট ও বাংলায় উপস্থাপন করা:
                       - 📖 **অধ্যায় / লেসন:** 
                       - 📄 **পৃষ্ঠা নম্বর:** 
                       - 🔢 **অংক নম্বর:** 
                       - 💡 **সমাধানের ইঙ্গিত (Hints):**
                    
                    যদি হুবহু না পাওয়া যায়, তবে সবচেয়ে কাছাকাছি মিল থাকা অংকটির বিবরণ দাও।
                    """

                    contents = [prompt]

                    # বইয়ের পেজ / PDF প্রক্রিয়াকরণ
                    for index, page in enumerate(uploaded_book_pages):
                        contents.append(f"\n[বইয়ের পেজ {index + 1}]:")
                        if page.type == "application/pdf":
                            contents.append({"mime_type": "application/pdf", "data": page.getvalue()})
                        else:
                            contents.append(Image.open(page))

                    # নির্দিষ্ট অংকের ছবি
                    contents.append("\n[খুঁজতে চাওয়া নির্দিষ্ট অংক]:")
                    contents.append(Image.open(query_image))

                    response = model.generate_content(contents)

                    # ফলাফল দেখানোর অংশ
                    st.balloons()
                    st.markdown("""
                    <div class="card" style="border-left: 6px solid #28a745;">
                        <h2 style="color: #28a745;">🎉 ফলাফল পেয়ে গেছি!</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(response.text)

                except Exception as e:
                    st.error(f"একটি ত্রুটি ঘটেছে: {e}")
else:
    st.warning("👈 অ্যাপটি শুরু করতে বামপাশের সাইডবারে আপনার **Gemini API Key** বসান।")
    
    
