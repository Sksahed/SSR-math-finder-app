
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="ম্যাথ বুক ফাইন্ডার", page_icon="📚", layout="centered")

st.title("📚 গণিত বইয়ের লেসন ও পৃষ্ঠা ফাইন্ডার")
st.write("তোমার বইয়ের পৃষ্ঠা বা PDF আপলোড করে রাখো, তারপর যেকোনো অংক স্ক্যান করলেই পৃষ্ঠা ও লেসন নম্বর পেয়ে যাবে!")

st.sidebar.header("⚙️ সেটআপ")
api_key = st.sidebar.text_input("Gemini API Key লিখুন:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    st.sidebar.markdown("---")
    st.sidebar.header("১. বইয়ের পৃষ্ঠা / PDF আপলোড")
    # এখানে pdf টাইপ যুক্ত করা হলো
    uploaded_book_pages = st.sidebar.file_uploader(
        "বইয়ের পৃষ্ঠা বা PDF ফাইল আপলোড করুন:", 
        type=["png", "jpg", "jpeg", "pdf"], 
        accept_multiple_files=True
    )

    st.header("২. নির্দিষ্ট অংক খুঁজুন")
    query_image = st.file_uploader(
        "যে অংকটি খুঁজতে চান তার ছবি আপলোড করুন:", 
        type=["png", "jpg", "jpeg"]
    )

    if st.button("🔍 অংকটি খুঁজে বের করো", type="primary"):
        if not uploaded_book_pages:
            st.error("⚠️ দয়া করে সাইডবার থেকে আগে বইয়ের অন্তত ১টি পৃষ্ঠা বা PDF আপলোড করুন!")
        elif not query_image:
            st.error("⚠️ দয়া করে যে অংকটি খুঁজতে চান তার ছবি আপলোড করুন!")
        else:
            with st.spinner("AI আপনার বইয়ের ফাইল স্ক্যান করছে... অনুগ্রহ করে অপেক্ষা করুন।"):
                try:
                    prompt = """
                    তুমি একজন দক্ষ সহকারী শিক্ষক। 
                    তোমাকে নিচে কিছু বইয়ের পৃষ্ঠা/PDF এবং শেষে একটি নির্দিষ্ট অংকের ছবি দেওয়া হয়েছে।
                    
                    তোমার কাজ হলো:
                    ১. অংকটি বইয়ের কোনো পৃষ্ঠার সাথে মিলে যায় কিনা তা ভালোভাবে চেক করা।
                    ২. উত্তরটি সহজ ভাষায় বাংলা ফরম্যাটে দেওয়া:
                       - 📖 **লেসন / অধ্যায়ের নাম:** 
                       - 📄 **পৃষ্ঠা নম্বর:** 
                       - 🔢 **অংক নম্বর:** 
                       - 💡 **সংক্ষিপ্ত হিন্টস/সমাধান:**
                    
                    যদি হুবহু না পাওয়া যায় তবে সবচেয়ে কাছের অংকটি কোন লেসনের তা জানিয়ে দাও।
                    """

                    contents = [prompt]

                    # বইয়ের ছবি বা PDF যোগ করা
                    for index, page in enumerate(uploaded_book_pages):
                        contents.append(f"\n[বইয়ের ফাইল {index + 1}]:")
                        if page.type == "application/pdf":
                            contents.append({"mime_type": "application/pdf", "data": page.getvalue()})
                        else:
                            contents.append(Image.open(page))

                    # নির্দিষ্ট অংকের ছবি যোগ করা
                    contents.append("\n[খুঁজতে চাওয়া অংক]:")
                    contents.append(Image.open(query_image))

                    response = model.generate_content(contents)

                    st.success("🎉 অংকটি সফলভাবে খুঁজে পাওয়া গেছে!")
                    st.markdown("---")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"একটি সমস্যা হয়েছে: {e}")
else:
    st.info("👈 শুরু করতে সাইডবারে আপনার **Gemini API Key** প্রদান করুন।")
    
