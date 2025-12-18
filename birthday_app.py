import streamlit as st
import time

# Настройка страницы для компактного отображения
st.set_page_config(
    page_title="🎁 С Днем Рождения, Вера!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Компактные стили CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden;
        font-family: 'Nunito', sans-serif;
    }

    .title {
        color: #333;
        font-size: 2.2em;
        margin-bottom: 10px;
        font-weight: 900;
    }

    .subtitle {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 10px;
    }

    .spins-counter {
        color: #ff6b6b;
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
    }

    .gift-display {
        font-size: 2em;
        font-weight: 900;
        margin: 15px 0;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .gift-options {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .gift-option {
        padding: 8px 10px;
        background: #e9ecef;
        border-radius: 10px;
        font-size: 1em;
        font-weight: 600;
        transition: all 0.3s ease;
        min-width: 180px;
        text-align: center;
        border: 1px solid #d1d9e0;  /* Серая рамка */
        box-shadow: 0 1px 2px rgba(0,0,0,0.05); /* Легкая тень для объема */
    }

    .gift-option.active {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        color: white;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(255,107,107,0.4);
    }

    .gift-option.claimed {
        background: linear-gradient(45deg, #4CAF50, #8BC34A);
        color: white;
        opacity: 0.9;
        position: relative;
        padding-left: 40px;
    }

    .gift-option.claimed:before {
        content: "✓";
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2em;
        font-weight: bold;
    }

    .gift-option.current {
        background: linear-gradient(45deg, #2196F3, #03A9F4);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(33,150,243,0.4);
        position: relative;
    }

    .gift-option.current:after {
        content: "🎯";
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2em;
    }

    .spinning {
        animation: smoothFloat 2s ease-in-out infinite;
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
    }

    .result {
        color: #e91e63;
        animation: pulseResult 1s ease infinite;
    }

    .button-container {
        margin: 15px 0 10px 0;
    }

    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        color: white;
        font-size: 1.2em;
        font-weight: 700;
        padding: 12px 40px;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 250px;
        margin: 0 auto;
        display: block;
        box-shadow: 0 8px 25px rgba(255,107,107,0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(255,107,107,0.6);
    }

    .stButton > button:active {
        transform: translateY(1px);
    }

    .stButton > button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .timer {
        color: #666;
        font-size: 1em;
        margin-top: 10px;
        height: 20px;
    }

    .progress-container {
        width: 100%;
        height: 6px;
        background: #e9ecef;
        border-radius: 3px;
        margin: 10px 0;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d);
        width: 0%;
        transition: width 0.3s ease;
        border-radius: 3px;
    }

    @keyframes smoothFloat {
        0%, 100% {
            transform: translateY(0);
            opacity: 1;
        }
        50% {
            transform: translateY(-7px);
            opacity: 0.7;
            filter: blur(0px);
        }
    }

    @keyframes pulseResult {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .final-message {
        font-size: 1.2em;
        color: #28a745;
        font-weight: 700;
        margin-top: 10px;
        animation: pulseResult 1.5s ease infinite;
    }

    /* Убираем лишние отступы Streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 600px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'current_gift' not in st.session_state:
    st.session_state.current_gift = "🏠 Пентхаус"
if 'spin_count' not in st.session_state:
    st.session_state.spin_count = 3  # Начальное количество спинов
if 'claimed_gifts' not in st.session_state:
    st.session_state.claimed_gifts = []  # Полученные подарки
if 'spin_results' not in st.session_state:
    st.session_state.spin_results = []  # Результаты спинов по порядку
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'spin_complete' not in st.session_state:
    st.session_state.spin_complete = False

# ВАЖНО: Время прокрутки спина как переменная
SPIN_DURATION = 5  # секунд

# Варианты подарков (добавлены "Деньги" и "Цветочки")
gifts = [
    "🏠 Пентхаус",
    "💐 Цветочки",
    "🚗 Феррари",
    "✈️ Мальдивы",
    "🖼️ Газета про именинника",
    "😏️ Собственный слуга (нигер)",
    "💰 Деньги",
    "✈️ Частный самолет"
]


# Определяем порядок выпадения подарков по спинам
def get_gift_for_spin(spin_number):
    """Возвращает подарок для конкретного спина"""
    if spin_number == 1:
        return "🖼️ Газета про именинника"
    elif spin_number == 2:
        return "💐 Цветочки"
    elif spin_number == 3:
        return "💰 Деньги"
    else:
        # Если спины закончились
        return None


# Заголовок
st.markdown('<h1 class="title">🎉 С Днем Рождения, Вера! 🎉</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Нажми "Крутить" и узнай свой подарок!</p>', unsafe_allow_html=True)

# Счетчик спинов
remaining_spins = max(0, 3 - len(st.session_state.spin_results))
st.markdown(f'<div class="spins-counter">🎯 Осталось спинов: {remaining_spins}</div>', unsafe_allow_html=True)

if st.session_state.spinning:
    # Вычисляем время прокрутки
    current_time = time.time()
    elapsed_time = current_time - st.session_state.start_time

    if elapsed_time < SPIN_DURATION:  # Прокрутка 7 секунд (используем переменную)
        # Последовательная смена подарков
        spin_speed = 0.1

        # Рассчитываем текущий индекс для анимации
        spin_cycle = int(elapsed_time * 3)  # 3 цикла в секунду
        current_index = spin_cycle % len(gifts)
        st.session_state.current_gift = gifts[current_index]

        # Отображаем текущий подарок с анимацией
        gift_display_class = "gift-display spinning"
        st.markdown(f'<div class="{gift_display_class}">{st.session_state.current_gift}</div>', unsafe_allow_html=True)

        # Прогресс бар (используем SPIN_DURATION вместо 3)
        progress = min(100, (elapsed_time / SPIN_DURATION) * 100)
        st.markdown(f'''
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
        ''', unsafe_allow_html=True)

        # Таймер (используем SPIN_DURATION вместо 7)
        remaining = SPIN_DURATION - elapsed_time
        st.markdown(f'<div class="timer">⏱️ Осталось: {remaining:.1f} сек.</div>', unsafe_allow_html=True)

        time.sleep(spin_speed)
        st.rerun()
    else:
        # Определяем какой подарок должен выпасть для текущего спина
        spin_number = len(st.session_state.spin_results) + 1
        result_gift = get_gift_for_spin(spin_number)

        # Останавливаем прокрутку
        st.session_state.spinning = False
        st.session_state.current_gift = result_gift
        st.session_state.spin_complete = True

        # Добавляем подарок в список полученных
        if result_gift and result_gift not in st.session_state.claimed_gifts:
            st.session_state.claimed_gifts.append(result_gift)

        # Сохраняем результат спина
        st.session_state.spin_results.append(result_gift)

        # ОБНОВЛЯЕМ счетчик спинов СРАЗУ
        st.session_state.spin_count -= 1  # Уменьшаем счетчик

        # Показываем результат
        gift_display_class = "gift-display result"
        st.markdown(f'<div class="{gift_display_class}">{st.session_state.current_gift}</div>', unsafe_allow_html=True)
        st.markdown('<div class="final-message">🎉 Твой подарок! 🎉</div>', unsafe_allow_html=True)

        # Полный прогресс бар
        st.markdown('''
                <div class="progress-container">
                    <div class="progress-bar" style="width: 100%"></div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div class="timer">✅ Прокрутка завершена!</div>', unsafe_allow_html=True)

        # СРАЗУ перерисовываем страницу для обновления счетчика
        st.rerun()

elif st.session_state.spin_complete:
    # Показываем результат после завершения
    gift_display_class = "gift-display result"
    st.markdown(f'<div class="{gift_display_class}">{st.session_state.current_gift}</div>', unsafe_allow_html=True)
    st.markdown('<div class="final-message">🎉 Твой подарок! 🎉</div>', unsafe_allow_html=True)

    st.markdown('<div class="timer">✅ Прокрутка завершена!</div>', unsafe_allow_html=True)

else:
    # Начальный экран
    gift_display_class = "gift-display"
    st.markdown(f'<div class="{gift_display_class}">🎁</div>', unsafe_allow_html=True)
    if remaining_spins > 0:
        st.markdown(f'<div class="timer">У тебя {remaining_spins} спина(ов). Удачи!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="timer">Спины закончились! Все подарки получены!</div>', unsafe_allow_html=True)

# Отображение всех вариантов подарков
st.markdown('<div class="gift-options">', unsafe_allow_html=True)
for gift in gifts:
    # Определяем класс для каждого варианта
    css_class = "gift-option"

    # Если подарок уже получен - зеленая галочка
    if gift in st.session_state.claimed_gifts:
        css_class += " claimed"
    # Если это текущий отображаемый подарок (во время или после прокрутки) - синий маркер
    elif (st.session_state.current_gift == gift and
          (st.session_state.spinning or st.session_state.spin_complete)):
        css_class += " current"

    st.markdown(f'<div class="{css_class}">{gift}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Кнопка
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# Проверяем, есть ли еще спины
has_spins_remaining = len(st.session_state.spin_results) < 3

if has_spins_remaining:
    if st.button("🎡 КРУТИТЬ!", key="spin_button", disabled=st.session_state.spinning):
        if not st.session_state.spinning:
            st.session_state.spinning = True
            st.session_state.start_time = time.time()
            st.session_state.spin_complete = False
            st.rerun()
else:
    st.markdown('<div class="spins-counter" style="color: #4CAF50;">🎉 Все подарки получены! 🎉</div>',
                unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Кнопка сброса (только после завершения всех спинов)
if not has_spins_remaining:
    if st.button("🔄 Начать заново", key="reset_button"):
        st.session_state.spinning = False
        st.session_state.spin_complete = False
        st.session_state.current_gift = "🏠 Пентхаус"
        st.session_state.spin_count = 3  # СБРАСЫВАЕМ счетчик на 3
        st.session_state.claimed_gifts = []
        st.session_state.spin_results = []
        st.rerun()

# Функция для автоматического обновления при прокрутке
if st.session_state.spinning:
    st.rerun()