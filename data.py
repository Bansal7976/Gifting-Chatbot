# data.py

products_for_ordering = {
    "For Her (Girlfriend, Sister, Friend)": {
        "Personalized Mug": {"description": "Ek sundar mug jisme custom photo aur message ho.", "price": 499},
        "Rose Gift Hamper": {"description": "Ek hamper jisme preserved roses, chocolates, aur ek scented candle ho.", "price": 1299},
        "Engraved Keychain": {"description": "Ek stylish keychain jisme aapke initials engrave kiye gaye hon.", "price": 349},
        "Customized Purse": {"description": "Ek chic purse jisme unka naam likha ho.", "price": 899},
        "Best Sister Mug": {"description": "Apna pyaar dikhane ke liye ek special mug.", "price": 450},
        "Jewelry Box": {"description": "Unke accessories store karne ke liye ek elegant box.", "price": 999},
        "Friendship Keychain Set": {"description": "Do matching keychains ka ek set, dosti ke liye.", "price": 599},
        "Funny Quote Mug": {"description": "Ek funny inside joke wala mug.", "price": 499},
        "Skincare Hamper": {"description": "Ek relaxing hamper jisme premium skincare products hon.", "price": 1599},
        "Handmade Dream Catcher": {"description": "Positive vibes ke liye ek khoobsurat dream catcher.", "price": 699},
    },
    "For Him (Boyfriend, Brother, Friend)": {
        "Personalized Wallet": {"description": "Ek high-quality wallet jisme unka naam ya initials engrave ho.", "price": 1199},
        "Gadget Hamper": {"description": "Cool gadgets, headphones, aur snacks wala ek fun hamper.", "price": 1499},
        "Custom Engraved Pen Set": {"description": "Ek professional aur elegant pen set.", "price": 1199},
        "Grooming Kit Hamper": {"description": "Ek complete grooming kit jisme sabhi essentials hon.", "price": 1799},
        "Superhero Themed Mug": {"description": "Unke favorite superhero wala ek cool mug.", "price": 550},
        "Leather Belt": {"description": "Ek classic aur stylish leather belt.", "price": 999},
    },
    "For Couples (Marriage, Anniversary)": {
        "Couple's Gift Hamper": {"description": "Naye couple ke liye wine glasses aur treats wala ek luxurious hamper.", "price": 2499},
        "Mr. & Mrs. Mugs": {"description": "Happy couple ke liye mugs ka ek set.", "price": 899},
        "Personalized Photo Frame": {"description": "Unke special din ko capture karne ke liye ek sundar frame.", "price": 799},
        "His & Hers Watch Set": {"description": "Ek elegant matching watch set, anniversary ke liye perfect.", "price": 3499},
        "Custom Date Keychain": {"description": "Ek keychain jisme unki special date (jaise anniversary) engrave ho.", "price": 499},
        "Adventure Scrapbook": {"description": "Apni saari yaadein sanjone ke liye ek scrapbook.", "price": 1299},
    },
    "For Parents": {
        "Family Photo Mug": {"description": "Ek family picture wala heartwarming mug.", "price": 550},
        "Gourmet Hamper": {"description": "Unke enjoy karne ke liye fine teas, coffees, aur snacks wala hamper.", "price": 1999},
        "Health & Wellness Hamper": {"description": "Healthy snacks aur immunity boosters wala ek thoughtful hamper.", "price": 2199},
        "Engraved Wooden Plaque": {"description": "'Best Mom & Dad' likha hua ek decorative wooden plaque.", "price": 1399},
    },
    "Budget Gifts (Under 700)": {
        "Chocolate Bouquet": {"description": "Alag alag chocolates se bana ek tasty bouquet.", "price": 599},
        "Personalized Diary": {"description": "Ek diary jiske cover par unka naam likha ho.", "price": 650},
        "Scented Candle Set": {"description": "Relaxing fragrance wali 3 candles ka set.", "price": 499},
        "Personalized Mug": {"description": "Ek sundar mug jisme custom photo aur message ho.", "price": 499},
        "Engraved Keychain": {"description": "Ek stylish keychain jisme aapke initials engrave kiye gaye hon.", "price": 349},
        "Friendship Keychain Set": {"description": "Do matching keychains ka ek set, dosti ke liye.", "price": 599},
        "Funny Quote Mug": {"description": "Ek funny inside joke wala mug.", "price": 499},
        "Handmade Dream Catcher": {"description": "Positive vibes ke liye ek khoobsurat dream catcher.", "price": 699},
    }
}

bb_creation_info = (
    "**BB CREATION** Sirsa, Haryana mein **Ritika Bansal** dwara shuru kiya gaya ek chhota handmade gifting brand hai.\n\n"
    "Hum customized, saste aur dil se banaye gaye gifts banate hain — jaise personalized mugs, engraved accessories, gift hampers, aur bhi bahut kuch.\n\n"
    "### Hamari Khas Baatein:\n"
    "- **Handmade with Love**: Har gift ko hum khud banate hain.\n"
    "- **Customization**: Aapki zaroorat ke hisaab se gifts taiyar kiye jaate hain.\n"
    "- **Delivery**: Hum poore **India** aur **Australia** mein delivery karte hain.\n"
    "- **Special Requests**: Surprise ya time-specific delivery ke liye hum special arrangements kar sakte hain (extra charges apply).\n\n"
    "Hamara mission gifting ko aasan, personal aur budget-friendly banana hai. ❤️"
)

def find_product_by_name(name):
    for cat, items in products_for_ordering.items():
        for pname, details in items.items():
            if pname.lower() == name.lower().strip():
                return cat, pname, details
    return None, None, None

def search_products(query, max_results=6):
    q = query.lower()
    results = []
    added_products = set()
    for cat, items in products_for_ordering.items():
        for pname, details in items.items():
            if pname in added_products:
                continue
            text = (pname + " " + details.get("description", "")).lower()
            if any(token in text for token in q.split()):
                results.append((cat, pname, details))
                added_products.add(pname)
    if not results:
        default_suggestions = list(products_for_ordering.get("Budget Gifts (Under 700)", {}).items())[:3] + \
                              list(products_for_ordering.get("For Her (Girlfriend, Sister, Friend)", {}).items())[:3]
        for pname, details in default_suggestions:
            if pname not in added_products:
                cat, _, _ = find_product_by_name(pname)
                results.append((cat, pname, details))
                added_products.add(pname)
    return results[:max_results]

# <--- BADLAV YAHAN SHURU HUA HAI --->
def calculate_total(order_details, is_special_request=False):
    """Order ka total calculate karta hai, special request charge ke saath."""
    total = 0
    for p in order_details.get("products", []):
        qty = p.get("quantity", 1)
        total += p.get("price", 0) * qty
    
    if is_special_request:
        total += 200  # Special request ke liye ₹200 add karein
        
    return total

def format_order_summary(order_details):
    """Cart ki summary ko format karta hai (bina special charge ke)."""
    if not order_details.get("products"):
        return "Aapka cart abhi khali hai."
        
    lines = [f"{i}. {p['name']} — {p.get('quantity', 1)} x ₹{p['price']} = ₹{p.get('quantity', 1) * p['price']}"
             for i, p in enumerate(order_details.get("products", []), start=1)]
    
    sub_total = calculate_total(order_details, is_special_request=False) # Yahan False pass karein
    lines.append(f"\n**Sub-Total: ₹{sub_total}**")
    return "\n".join(lines)
# <--- BADLAV YAHAN KHATAM HUA HAI --->