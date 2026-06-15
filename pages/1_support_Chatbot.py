import streamlit as st
from data.products import products

st.set_page_config(
    page_title="Support Chatbot",
    page_icon="💬"
)

st.title("💬 MiniStore Support Assistant")

# ------------------------------------------
# Chat History
# ------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Hello! I'm MiniStore Support. How can I help you today?"
        }
    ]

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------
# Rule Based Bot
# ------------------------------------------

def generate_response(user_input):

    text = user_input.lower()

    # Product Search

    for product in products:

        if product["name"].lower() in text:

            return (
                f"📦 {product['name']}\n\n"
                f"Price: ${product['price']}\n\n"
                f"{product['description']}"
            )

    # Product Questions

    if "product" in text:
        names = [p["name"] for p in products]

        return (
            "We currently sell:\n\n- "
            + "\n- ".join(names)
        )

    # Delivery

    elif any(word in text for word in [
        "delivery",
        "shipping",
        "when will it arrive"
    ]):

        return (
            "🚚 Standard delivery takes 3-5 business days. "
            "Express delivery takes 1-2 business days."
        )

    # Refunds

    elif "refund" in text:

        return (
            "💰 Refunds are processed within 5-7 business days after approval."
        )

    # Returns

    elif "return" in text:

        return (
            "↩️ Products can be returned within 30 days of delivery."
        )

    # Payment

    elif any(word in text for word in [
        "payment",
        "upi",
        "card",
        "credit card",
        "debit card"
    ]):

        return (
            "💳 We accept UPI, Credit Cards, Debit Cards, Net Banking, and Wallets."
        )

    # Order Status

    elif any(word in text for word in [
        "order status",
        "track order",
        "where is my order"
    ]):

        return (
            "📦 Please provide your Order ID. "
            "For this demo, all orders are currently marked as 'In Transit'."
        )

    return (
        "I'm here to help with products, orders, delivery, returns, refunds, and payments."
    )

# ------------------------------------------
# User Input
# ------------------------------------------

prompt = st.chat_input(
    "Ask something about products, delivery, refunds..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = generate_response(prompt)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response)