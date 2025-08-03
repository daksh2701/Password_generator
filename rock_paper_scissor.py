import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors Arena",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E4057;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #6C757D;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .choice-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .choice-button {
        background: linear-gradient(145deg, #f0f0f0, #cacaca);
        border: none;
        border-radius: 20px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        min-width: 120px;
        text-align: center;
    }
    
    .choice-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
    }
    
    .choice-emoji {
        font-size: 3rem;
        display: block;
        margin-bottom: 10px;
    }
    
    .choice-name {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .vs-container {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .player-choice {
        display: inline-block;
        margin: 0 2rem;
        text-align: center;
    }
    
    .choice-display {
        font-size: 4rem;
        margin-bottom: 10px;
        display: block;
        animation: bounce 0.6s ease-in-out;
    }
    
    .vs-text {
        font-size: 2rem;
        font-weight: bold;
        margin: 0 1rem;
        vertical-align: middle;
    }
    
    .result-container {
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        font-size: 1.5rem;
        font-weight: bold;
        animation: fadeIn 0.5s ease-in;
    }
    
    .result-win {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
    }
    
    .result-lose {
        background: linear-gradient(135deg, #dc3545, #fd7e14);
        color: white;
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3);
    }
    
    .result-tie {
        background: linear-gradient(135deg, #6c757d, #495057);
        color: white;
        box-shadow: 0 8px 25px rgba(108, 117, 125, 0.3);
    }
    
    .score-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        border-left: 5px solid #667eea;
    }
    
    .score-item {
        display: flex;
        justify-content: space-between;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        80% { transform: translateY(-10px); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .game-rules {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .emoji-large {
        font-size: 1.5rem;
    }
    
    @media (max-width: 768px) {
        .choice-container {
            flex-direction: column;
            align-items: center;
        }
        
        .vs-container {
            padding: 1rem;
        }
        
        .choice-display {
            font-size: 3rem;
        }
        
        .vs-text {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_wins' not in st.session_state:
    st.session_state.user_wins = 0
if 'computer_wins' not in st.session_state:
    st.session_state.computer_wins = 0
if 'ties' not in st.session_state:
    st.session_state.ties = 0
if 'total_games' not in st.session_state:
    st.session_state.total_games = 0
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Game logic
def play_game(user_choice):
    choices = {0: "Rock", 1: "Paper", 2: "Scissors"}
    emojis = {0: "🪨", 1: "📄", 2: "✂️"}
    
    computer_choice = random.randint(0, 2)
    
    # Determine winner
    if user_choice == computer_choice:
        result = "tie"
        st.session_state.ties += 1
    elif (user_choice == 0 and computer_choice == 2) or \
         (user_choice == 1 and computer_choice == 0) or \
         (user_choice == 2 and computer_choice == 1):
        result = "win"
        st.session_state.user_wins += 1
    else:
        result = "lose"
        st.session_state.computer_wins += 1
    
    st.session_state.total_games += 1
    
    # Store game result
    game_data = {
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }
    
    st.session_state.game_history.insert(0, game_data)
    if len(st.session_state.game_history) > 10:  # Keep only last 10 games
        st.session_state.game_history.pop()
    
    st.session_state.last_result = game_data
    
    return game_data

def reset_game():
    st.session_state.user_wins = 0
    st.session_state.computer_wins = 0
    st.session_state.ties = 0
    st.session_state.total_games = 0
    st.session_state.game_history = []
    st.session_state.last_result = None

# Main UI
st.markdown('<h1 class="main-header">🎮 Rock Paper Scissors Arena</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Challenge the computer and test your luck!</p>', unsafe_allow_html=True)

# Game rules
with st.expander("📋 Game Rules", expanded=False):
    st.markdown("""
    <div class="game-rules">
    <strong>How to Play:</strong><br>
    🪨 <strong>Rock</strong> crushes ✂️ Scissors<br>
    📄 <strong>Paper</strong> covers 🪨 Rock<br>
    ✂️ <strong>Scissors</strong> cuts 📄 Paper<br><br>
    <strong>Choose your weapon and try to beat the computer!</strong>
    </div>
    """, unsafe_allow_html=True)

# Choice buttons
st.markdown("### Make Your Choice:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨\n**ROCK**", key="rock", help="Rock crushes Scissors"):
        game_result = play_game(0)

with col2:
    if st.button("📄\n**PAPER**", key="paper", help="Paper covers Rock"):
        game_result = play_game(1)

with col3:
    if st.button("✂️\n**SCISSORS**", key="scissors", help="Scissors cuts Paper"):
        game_result = play_game(2)

# Display last game result
if st.session_state.last_result:
    result_data = st.session_state.last_result
    choices = {0: "Rock", 1: "Paper", 2: "Scissors"}
    emojis = {0: "🪨", 1: "📄", 2: "✂️"}
    
    # Battle display
    st.markdown(f"""
    <div class="vs-container">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <div class="player-choice">
                <div><strong>YOU</strong></div>
                <span class="choice-display">{emojis[result_data['user_choice']]}</span>
                <div>{choices[result_data['user_choice']]}</div>
            </div>
            <div class="vs-text">VS</div>
            <div class="player-choice">
                <div><strong>COMPUTER</strong></div>
                <span class="choice-display">{emojis[result_data['computer_choice']]}</span>
                <div>{choices[result_data['computer_choice']]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Result display
    if result_data['result'] == 'win':
        st.markdown(f"""
        <div class="result-container result-win">
            🎉 CONGRATULATIONS! YOU WON! 🎉
        </div>
        """, unsafe_allow_html=True)
    elif result_data['result'] == 'lose':
        st.markdown(f"""
        <div class="result-container result-lose">
            😔 You Lost! Better Luck Next Time!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-container result-tie">
            🤝 It's a Tie! Great Minds Think Alike!
        </div>
        """, unsafe_allow_html=True)

# Score display
if st.session_state.total_games > 0:
    st.markdown("### 📊 Current Score")
    
    win_rate = (st.session_state.user_wins / st.session_state.total_games) * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="score-container">
            <div class="score-item">
                <span><span class="emoji-large">🏆</span> Your Wins:</span>
                <span><strong>{st.session_state.user_wins}</strong></span>
            </div>
            <div class="score-item">
                <span><span class="emoji-large">🤖</span> Computer Wins:</span>
                <span><strong>{st.session_state.computer_wins}</strong></span>
            </div>
            <div class="score-item">
                <span><span class="emoji-large">🤝</span> Ties:</span>
                <span><strong>{st.session_state.ties}</strong></span>
            </div>
            <div class="score-item">
                <span><span class="emoji-large">🎮</span> Total Games:</span>
                <span><strong>{st.session_state.total_games}</strong></span>
            </div>
            <div class="score-item">
                <span><span class="emoji-large">📈</span> Win Rate:</span>
                <span><strong>{win_rate:.1f}%</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Progress bars for visual representation
        st.metric("Win Rate", f"{win_rate:.1f}%")
        st.progress(win_rate / 100)
        
        if win_rate >= 70:
            st.success("🔥 You're on fire!")
        elif win_rate >= 50:
            st.info("⚡ Good performance!")
        else:
            st.warning("💪 Keep trying!")

# Control buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Play Again", type="primary"):
        st.rerun()

with col2:
    if st.button("🗑️ Reset Game"):
        reset_game()
        st.rerun()

# Game history
if st.session_state.game_history:
    with st.expander("📜 Recent Games", expanded=False):
        st.markdown("### Last 10 Games")
        
        for i, game in enumerate(st.session_state.game_history[:10]):
            choices = {0: "Rock", 1: "Paper", 2: "Scissors"}
            emojis = {0: "🪨", 1: "📄", 2: "✂️"}
            
            result_emoji = "🏆" if game['result'] == 'win' else "😔" if game['result'] == 'lose' else "🤝"
            result_text = "Won" if game['result'] == 'win' else "Lost" if game['result'] == 'lose' else "Tied"
            
            st.markdown(f"""
            **Game {i+1}** ({game['timestamp']}) - {result_emoji} {result_text}  
            You: {emojis[game['user_choice']]} {choices[game['user_choice']]} vs 
            Computer: {emojis[game['computer_choice']]} {choices[game['computer_choice']]}
            """)

# Fun facts
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; font-size: 0.9rem;">
    <strong>💡 Fun Fact:</strong> Rock Paper Scissors is called "Rochambeau" in some places, 
    named after the French general Comte de Rochambeau!
</div>
""", unsafe_allow_html=True)