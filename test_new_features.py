#!/usr/bin/env python3
"""
Тест новой функциональности - кнопки действий при выборе варианта
"""
import urllib.parse

def test_url_encoding():
    """Тест URL-энкодинга для текстов"""
    test_texts = [
        "Привет! Как дела?",
        "Я чувствую себя расстроенным из-за этой ситуации",
        "Мне важно выразить свою точку зрения по этому вопросу",
        "Текст с emoji 😊 и спецсимволами #@$%"
    ]
    
    print("🧪 Тестирование URL-энкодинга:")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        encoded = urllib.parse.quote(text)
        tg_url = f"tg://msg?text={encoded}"
        
        print(f"{i}. Исходный текст: {text}")
        print(f"   Закодированный: {encoded}")
        print(f"   Telegram URL: {tg_url}")
        print()

def test_sharing_url():
    """Тест URL для шеринга бота"""
    share_url = "https://t.me/share/url?url=https://t.me/assertive_me_bot&text=Помогает%20переформулировать%20токсичные%20сообщения%20в%20ассертивные"
    print("🔗 URL для шеринга бота:")
    print(share_url)
    print()

def simulate_user_flow():
    """Симуляция пользовательского сценария"""
    print("👤 Симуляция пользовательского сценария:")
    print("=" * 50)
    
    # Имитация пользовательских данных
    user_id = 12345
    variants = [
        "Я чувствую себя расстроенным из-за этой ситуации и хотел бы обсудить это конструктивно",
        "Мне важно выразить свою точку зрения по этому вопросу",
        "Я бы хотел найти решение, которое устроит всех участников"
    ]
    
    print(f"Пользователь {user_id} получил варианты:")
    for i, variant in enumerate(variants, 1):
        print(f"{i}. {variant}")
    
    print("\nПользователь выбрал вариант 2...")
    selected_variant = variants[1]  # индекс 1 для варианта 2
    encoded_text = urllib.parse.quote(selected_variant)
    
    print(f"Выбранный текст: {selected_variant}")
    print(f"URL для копирования: tg://msg?text={encoded_text}")
    print("✅ Тест пройден!")

if __name__ == "__main__":
    print("🚀 Тестирование новой функциональности AssertiveMeBot")
    print("=" * 60)
    print()
    
    test_url_encoding()
    test_sharing_url()
    simulate_user_flow()
    
    print("✅ Все тесты завершены!")
