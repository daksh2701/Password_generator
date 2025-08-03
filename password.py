import streamlit as st
import random

# Set page config
st.set_page_config(
    page_title="Password Generator",
    page_icon="🔐",
    layout="centered"
)

# Title and description
st.title("🔐 Python Password Generator")
st.write("Generate secure passwords with custom settings")

# Create input fields using Streamlit widgets
col1, col2, col3 = st.columns(3)

with col1:
    x = st.number_input("How many letters?", min_value=0, max_value=50, value=8, step=1)

with col2:
    x1 = st.number_input("How many numbers?", min_value=0, max_value=20, value=2, step=1)

with col3:
    x2 = st.number_input("How many symbols?", min_value=0, max_value=20, value=2, step=1)

# Password generation logic
letters = ['I','b','g','l','Y','J','m','v','U','Z','N','D','j','r','P','d','S','X','e','n','F','W','w','o','Q','u','B','y','K','R','q','k','s','G','T','x','f','a','c','C','t','O','M','p','A','H','V','z','h','i','E','L']
numbers = ['1','2','3','4','5','6','7','8','9','0']
symbols = ['!','@','#','$','%','^','&','*']

# Generate password button
if st.button("Generate Password", type="primary"):
    if x + x1 + x2 == 0:
        st.error("Please select at least one character type!")
    else:
        password_list = []
        
        # Add letters
        for char in range(0, x):
            password_list.append(random.choice(letters))
        
        # Add numbers
        for char in range(0, x1):
            password_list.append(random.choice(numbers))
        
        # Add symbols
        for char in range(0, x2):
            password_list.append(random.choice(symbols))
        
        # Shuffle and create password
        random.shuffle(password_list)
        password = "".join(password_list)
        
        # Display the generated password
        st.success("Password generated successfully!")
        st.code(password, language=None)
        
        # Display password strength info
        total_chars = len(password)
        st.info(f"Password length: {total_chars} characters")
        
        # Show composition
        st.write("**Password composition:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Letters", x)
        with col2:
            st.metric("Numbers", x1)
        with col3:
            st.metric("Symbols", x2)

# Add some helpful information
st.markdown("---")
st.markdown("### Tips for Strong Passwords:")
st.markdown("""
- Use at least 12 characters
- Include a mix of letters, numbers, and symbols
- Avoid common words or personal information
- Use unique passwords for different accounts
""")

# Show available character sets
with st.expander("View available characters"):
    st.write("**Letters:**", "".join(letters))
    st.write("**Numbers:**", "".join(numbers))
    st.write("**Symbols:**", "".join(symbols))