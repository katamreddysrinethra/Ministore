import streamlit as st
from openai import OpenAI
from data.products import products

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="MiniStore Support",
    page_icon="💬"
)

st.title("💬 MiniStore AI Support Assistant")

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error(
        "OPENAI_API_KEY not found in .streamlit/secrets.toml"
    )
    st.stop()
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ---------------------------------------------------
# BUILD PRODUCT CATALOG
# ---------------------------------------------------

catalog = ""

for product in products:
    catalog += f"""
Product Name: {product['name']}
Price: ${product['price']}
Category: {product['category']}
Description: {product['description']}

"""

# ---------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------

SYSTEM_PROMPT = f"""
You are MiniStore's professional customer support representative.

Your job is to help customers with:

- Products
- Orders
- Delivery
- Shipping
- Refunds
- Returns
- Payments
- Store policies

MiniStore Product Catalog:

{catalog}

Rules:

1. Only answer questions related to MiniStore.
2. Use the product catalog when answering product questions.
3. Be professional, friendly, and concise.
4. If the user asks unrelated questions such as:
   - coding
   - mathematics
   - politics
   - celebrities
   - general knowledge
   - personal advice

   politely respond:

   "I'm MiniStore's support assistant and can only help with products, orders, delivery, refunds, returns, payments, and other store-related questions."

5. Never pretend to know order information that was not provided.
6. If a customer asks about order status, ask for an order ID.
"""

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to MiniStore Support.\n\n"
                "I can help with products, orders, delivery, "
                "refunds, returns, and payments."
            )
        }
    ]

# ---------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input(
    "Ask about products, orders, delivery, refunds..."
)

if prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )

        assistant_reply = response.choices[0].message.content

    except Exception as e:

        assistant_reply = f"""
❌ Error connecting to OpenAI.

Details:
{str(e)}
"""

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)