import streamlit as st
from data.products import products

st.set_page_config(
    page_title="MiniStore",
    page_icon="🛍️",
    layout="wide"
)

# ------------------------------------------------
# CSS
# ------------------------------------------------

st.markdown("""
<style>

.hero {
    background: linear-gradient(135deg,#4F46E5,#7C3AED);
    padding:40px;
    border-radius:20px;
    color:white;
    text-align:center;
}

.product-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

/* Floating Support Button */

.support-btn{
    position:fixed;
    bottom:30px;
    right:30px;
    z-index:999;
}

.support-btn a{
    text-decoration:none;
    background:#4F46E5;
    color:white;
    padding:15px 25px;
    border-radius:50px;
    font-weight:bold;
    box-shadow:0 4px 15px rgba(0,0,0,0.25);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Sidebar
# ------------------------------------------------

st.sidebar.title("🛍️ MiniStore")

categories = ["All"] + list(
    sorted(set(p["category"] for p in products))
)

selected = st.sidebar.selectbox(
    "Browse Categories",
    categories
)

st.sidebar.markdown("---")

st.sidebar.subheader("🛒 Cart Summary")
st.sidebar.write("Items: 3")
st.sidebar.write("Total: $249.97")

# ------------------------------------------------
# Hero
# ------------------------------------------------

st.markdown("""
<div class="hero">
<h1>🛍️ MiniStore</h1>
<p>Your One Stop Online Store</p>
</div>
""", unsafe_allow_html=True)

st.write("")

st.header("Featured Products")

# Filter products

if selected == "All":
    filtered = products
else:
    filtered = [
        p for p in products
        if p["category"] == selected
    ]

cols = st.columns(3)

for i, product in enumerate(filtered):

    with cols[i % 3]:

        st.markdown(f"""
        <div class="product-card">
            <h4>{product['name']}</h4>
            <p><b>${product['price']}</b></p>
            <p>{product['description']}</p>
            <small>{product['category']}</small>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Add to Cart",
            key=i
        )

# ------------------------------------------------
# Floating Support Button
# ------------------------------------------------
# ------------------------------------------------
# Floating Support Button
# ------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

if st.button("💬 Support Chatbot"):
    st.switch_page("pages/1_Support_Chatbot.py")