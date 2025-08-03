
import streamlit as st
import random
import string



# Page configuration
st.set_page_config(
    page_title="SecurePass Generator",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E4057;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #6C757D;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .password-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .password-text {
        color: white;
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        font-weight: bold;
        word-break: break-all;
        margin: 0;
    }
    
    .strength-indicator {
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .strength-weak {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .strength-medium {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .strength-strong {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

def calculate_password_strength(password):
    """Calculate password strength based on various criteria"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")
    
    # Character variety checks
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Include lowercase letters")
        
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Include uppercase letters")
        
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include numbers")
        
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Include special characters")
    
    # Determine strength level
    if score >= 5:
        return "Strong", "strength-strong", "🟢 Strong Password"
    elif score >= 3:
        return "Medium", "strength-medium", "🟡 Medium Strength"
    else:
        return "Weak", "strength-weak", "🔴 Weak Password"

def generate_password(num_letters, num_symbols, num_numbers):
    """Generate a secure password with specified criteria"""
    # Use string constants for better security
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password_list = []
    
    # Add characters based on user input
    for _ in range(num_letters):
        password_list.append(random.choice(letters))
    
    for _ in range(num_symbols):
        password_list.append(random.choice(symbols))
    
    for _ in range(num_numbers):
        password_list.append(random.choice(numbers))
    
    # Shuffle for better security
    random.shuffle(password_list)
    
    return ''.join(password_list)

# Main UI
st.markdown('<h1 class="main-header">🔐 SecurePass Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create strong, secure passwords with customizable options</p>', unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Password Configuration")
    
    # Input controls with validation
    num_letters = st.slider(
        "Number of Letters (a-z, A-Z)",
        min_value=1,
        max_value=50,
        value=8,
        help="Include both uppercase and lowercase letters"
    )
    
    num_numbers = st.slider(
        "Number of Numbers (0-9)",
        min_value=0,
        max_value=20,
        value=2,
        help="Add numeric characters for better security"
    )
    
    num_symbols = st.slider(
        "Number of Symbols (!@#$%^&*)",
        min_value=0,
        max_value=20,
        value=2,
        help="Special characters significantly increase password strength"
    )
    
    total_length = num_letters + num_numbers + num_symbols
    st.info(f"Total password length: **{total_length}** characters")

with col2:
    st.markdown("### Security Tips")
    st.markdown("""
    <div class="info-box">
    <strong>🛡️ Best Practices:</strong><br>
    • Use at least 12 characters<br>
    • Mix letters, numbers & symbols<br>
    • Avoid personal information<br>
    • Use unique passwords<br>
    • Consider a password manager
    </div>
    """, unsafe_allow_html=True)

# Generate password button
if st.button("🎲 Generate Secure Password", type="primary"):
    if total_length > 0:
        password = generate_password(num_letters, num_symbols, num_numbers)
        st.session_state.generated_password = password
        
        # Add to history (keep last 5)
        if password not in st.session_state.password_history:
            st.session_state.password_history.insert(0, password)
            if len(st.session_state.password_history) > 5:
                st.session_state.password_history.pop()
    else:
        st.error("Please select at least one character type!")

# Display generated password
if st.session_state.generated_password:
    st.markdown("### Generated Password")
    
    # Password display
    st.markdown(f"""
    <div class="password-display">
        <p class="password-text">{st.session_state.generated_password}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Password strength indicator
    strength, strength_class, strength_text = calculate_password_strength(st.session_state.generated_password)
    st.markdown(f"""
    <div class="strength-indicator {strength_class}">
        {strength_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Copy to Clipboard"):
            try:
                pyperclip.copy(st.session_state.generated_password)
                st.success("Password copied to clipboard!")
            except:
                st.warning("Manual copy: Select and copy the password above")
    
    with col2:
        if st.button("🔄 Generate New"):
            password = generate_password(num_letters, num_symbols, num_numbers)
            st.session_state.generated_password = password
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear"):
            st.session_state.generated_password = ""
            st.rerun()

# Password history
if st.session_state.password_history:
    with st.expander("📜 Recent Passwords"):
        for i, pwd in enumerate(st.session_state.password_history[:5]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.code(pwd)
            with col2:
                if st.button("📋", key=f"copy_{i}", help="Copy this password"):
                    try:
                        pyperclip.copy(pwd)
                        st.success("Copied!")
                    except:
                        st.warning("Manual copy needed")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; font-size: 0.9rem;">
    <strong>⚠️ Security Notice:</strong> Store your passwords securely using a password manager.<br>
    Never share passwords or store them in plain text files.
</div>
""", unsafe_allow_html=True)
