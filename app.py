import streamlit as st
import re
import random 
from datetime import datetime, time
from data import (
    products_for_ordering,
    search_products,
    find_product_by_name,
    format_order_summary,
    calculate_total,
    bb_creation_info
)

st.set_page_config(page_title="BB CREATION", page_icon="🎁")

GREETING_RESPONSES = [
    "Hello! Welcome to BB CREATION — main aapka dost hoon, aapka gift advisor. ✨\nAap neeche di gayi categories mein se choose kar sakte hain ya type karke search kar sakte hain.",
    "Namaste! BB CREATION mein aapka swagat hai. Main aapki gifts choose karne mein kaise madad kar sakta hoon?",
    "Hi there! Main BB hoon, aapka personal gift advisor. Chaliye aapke liye ek perfect gift dhoondhte hain! Aap categories browse kar sakte hain ya kuch search kar sakte hain."
]
SUGGESTION_RESPONSES = [
    "Aapke search ke hisab se, yeh kuch options hain:",
    "Maine aapke liye yeh kuch suggestions dhoondhe hain:",
    "Yeh kuch gifts hain jo aapko pasand aa sakte hain:",
    "Dekhiye, mujhe yeh kuch mila hai. Shayad inmein se koi aapke kaam ka ho."
]
CATEGORY_RESPONSES = {
    "For Parents": "Apne **Parents** ke liye, aap inmein se choose kar sakte hain:",
    "For Her (Girlfriend, Sister, Friend)": "Unke liye yeh kuch khaas tohfe hain:",
    "For Him (Boyfriend, Brother, Friend)": "Unke liye yeh kuch behtareen options hain:",
    "For Couples (Marriage, Anniversary)": "Couples ke liye yeh kuch special gifts hain:",
    "Budget Gifts (Under 700)": "Aapke budget mein yeh kuch acche options hain:"
}
NO_RESULTS_RESPONSES = [
    "Sorry, mujhe isse milta-julta koi product nahi mila. Kya aap kuch aur try karenge?",
    "Maaf kijiye, is search se related koi gift nahi mila. Aap keywords badal kar try kar sakte hain.",
    "Hmm, mujhe kuch khaas nahi mila. Aap 'mug' ya 'anniversary gift' jaisa kuch aur search karke dekhein?"
]


# --- Category Keywords ---
CATEGORY_KEYWORDS = {
    "For Parents": ["parent", "dad", "father", "mom", "mother", "maa", "papa"],
    "For Her (Girlfriend, Sister, Friend)": ["girlfriend", "sister", "her", "female", "women", "ladies"],
    "For Him (Boyfriend, Brother, Friend)": ["boyfriend", "brother", "him", "male", "men", "gentleman"],
    "For Couples (Marriage, Anniversary)": ["couple", "marriage", "anniversary", "wedding", "partner", "spouse"],
    "Budget Gifts (Under 700)": ["budget", "cheap", "affordable", "under 700", "sasta", "kam daam"],
}

def detect_category(user_text):
    text = user_text.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cat
    return None

# --- Initialize Session State ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'initial_query'
    st.session_state.order_details = {"products": []}
    st.session_state.messages = [{"role": "assistant", "content": random.choice(GREETING_RESPONSES)}]
    st.session_state.product_to_add = None
    st.session_state.items_to_show = {}

st.title("🎁 BB CREATION Gift Advisor")
st.sidebar.header("Your Cart")
cart_summary = format_order_summary(st.session_state.order_details)
st.sidebar.markdown(cart_summary)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def show_category_products(category_name):
    items = products_for_ordering.get(category_name, {})
    response = CATEGORY_RESPONSES.get(category_name, f"**{category_name}** ke liye yeh products hain:")
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.stage = 'category_selection'
    st.session_state.items_to_show = items
    st.rerun()

def handle_product_selection(product_name):
    _, prod_name, details = find_product_by_name(product_name)
    if details:
        st.session_state.product_to_add = prod_name
        st.session_state.stage = 'quantity_selection'
        st.session_state.items_to_show = {}
        st.rerun()

def add_to_cart(product_name, quantity):
    _, prod_name, details = find_product_by_name(product_name)
    order = st.session_state.order_details
    found = any(p['name'] == prod_name for p in order['products'])
    if found:
        for p in order['products']:
            if p['name'] == prod_name: p['quantity'] += quantity
    else:
        order['products'].append({"name": prod_name, "price": details['price'], "quantity": quantity})
    st.session_state.order_details = order
    st.session_state.product_to_add = None
    st.session_state.stage = 'ask_more_or_proceed'
    st.rerun()

def restart_conversation():
    st.session_state.stage = 'initial_query'
    st.session_state.order_details = {"products": []}
    st.session_state.messages = [{"role": "assistant", "content": "Okay, session restart ho gaya. Chaliye phir se shuru karte hain! 👋"}]
    st.session_state.items_to_show = {}
    st.rerun()

if st.session_state.stage == 'initial_query':
    st.info("Aap kiske liye gift dhundh rahe hain? Choose a category below:")
    cols = st.columns(3)
    for i, category in enumerate(CATEGORY_KEYWORDS.keys()):
        if cols[i % 3].button(category, key=f"cat_button_{i}"):
            show_category_products(category)

elif st.session_state.stage == 'category_selection':
    for pname, det in st.session_state.get('items_to_show', {}).items():
        if st.button(f"{pname} (₹{det['price']})", key=f"prod_btn_{pname}"):
            handle_product_selection(pname)

elif st.session_state.stage == 'quantity_selection':
    prod_name = st.session_state.product_to_add
    st.info(f"Aapne **{prod_name}** select kiya hai. Kitne pieces chahiye?")
    qty = st.number_input("Quantity", min_value=1, value=1, step=1, key="qty_input")
    if st.button(f"Add {qty} to Cart"):
        add_to_cart(prod_name, qty)

elif st.session_state.stage == 'ask_more_or_proceed':
    st.info("Kya aapko aur kuch add karna hai ya order finalize karein?")
    col1, col2 = st.columns(2)
    if col1.button("➕ Aur Add Karein"):
        st.session_state.stage = 'initial_query'
        st.rerun()
    if col2.button("✅ Aage Badhein (Checkout)"):
        st.session_state.stage = 'contact_info'
        st.rerun()

elif st.session_state.stage == 'contact_info':
    with st.form("contact_form"):
        st.info("Checkout ke liye, please neeche di gayi details bharein.")
        name = st.text_input("Aapka poora naam:")
        phone = st.text_input("Aapka contact number (e.g., 91XXXXXXXXXX):")
        address = st.text_area("Delivery address:")
        special_request = st.radio("Kya yeh ek special order hai (Surprise/Timed Delivery)?", ('No', 'Yes'), horizontal=True)
        delivery_date, delivery_time = None, None
        if special_request == 'Yes':
            st.warning("Special/Timed delivery ke liye ₹200 extra charge lagega.")
            delivery_date = st.date_input("Delivery Date", min_value=datetime.today())
            delivery_time = st.time_input("Delivery Time", value=time(12, 00))
        submitted = st.form_submit_button("Confirm Order")
        if submitted:
            if not (name and phone and address): st.error("Please sabhi fields bharein.")
            elif not re.match(r'^\+?[0-9]{10,12}$', phone): st.error("Invalid phone number format.")
            else:
                order = st.session_state.order_details
                order.update({'customer_name': name, 'contact_phone': phone, 'address': address})
                is_special = (special_request == 'Yes')
                order['special_request'] = is_special
                sub_total = calculate_total(order, is_special_request=False)
                final_total = calculate_total(order, is_special_request=is_special)
                summary_lines = [f"- {p['name']} ({p['quantity']} x ₹{p['price']})" for p in order['products']]
                summary_text = "\n".join(summary_lines)
                final_message = f"**Dhanyavaad! Aapka order confirm ho gaya hai.** ✅\n---\n"
                final_message += f"**Order Details:**\n{summary_text}\n\n**Sub-Total:** ₹{sub_total}\n"
                if is_special:
                    final_message += "**Special Delivery Charge:** ₹200\n"
                    order.update({
                        'delivery_date': delivery_date.strftime('%d-%b-%Y'),
                        'delivery_time': delivery_time.strftime('%I:%M %p')
                    })
                final_message += f"**Grand Total: ₹{final_total}**\n---\n"
                final_message += f"**Delivery Details:**\n- **Naam:** {name}\n- **Address:** {address}\n- **Contact:** {phone}\n"
                if is_special:
                    final_message += f"- **Delivery Time:** {order['delivery_date']} at {order['delivery_time']}\n"
                final_message += "---\nHum aapse jald hi confirmation ke liye sampark karenge."
                st.session_state.messages.append({"role": "assistant", "content": final_message})
                st.session_state.stage = 'order_confirmed'
                st.rerun()

elif st.session_state.stage == 'order_confirmed':
    st.success("Aapka order successfully place ho gaya hai!")
    if st.button("Start New Order"):
        restart_conversation()

if prompt := st.chat_input("Search for a gift or product..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_text = prompt.strip().lower()
    
    if any(tok in user_text for tok in ["about bb", "bb creation", "who are you"]):
        st.session_state.messages.append({"role": "assistant", "content": bb_creation_info})
        st.rerun()
    elif any(tok in user_text for tok in ["exit", "quit", "cancel", "bye", "start over"]):
        restart_conversation()
    else:
        st.session_state.items_to_show = {}
        detected_cat = detect_category(user_text)
        if detected_cat:
            show_category_products(detected_cat)
        else:
            results = search_products(user_text)
            if results:
                # <--- BADLAV: Random suggestion response --->
                st.session_state.messages.append({"role": "assistant", "content": random.choice(SUGGESTION_RESPONSES)})
                st.session_state.stage = 'category_selection'
                st.session_state.items_to_show = {pname: det for _, pname, det in results}
                st.rerun()
            else:
                st.session_state.messages.append({"role": "assistant", "content": random.choice(NO_RESULTS_RESPONSES)})
                st.rerun()