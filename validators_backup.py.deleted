import re
from config import MIN_MESSAGE_LENGTH, MAX_MESSAGE_LENGTH

class MessageValidator:
    @staticmethod
    def validate_message_length(text):
        """Проверка длины сообщения"""
        if len(text) < MIN_MESSAGE_LENGTH:
            return False, "too_short"
        elif len(text) > MAX_MESSAGE_LENGTH:
            return False, "too_long"
        return True, "valid"
    
    @staticmethod
    def has_potential_for_reformulation(text):
        """УЛЬТРА-МЯГКАЯ проверка - пропускаем ВСЕ осмысленные сообщения"""
        text_stripped = text.strip()
        
        # Отклоняем только совсем бессмысленные случаи:
        
        # 1. Пустые сообщения
        if not text_stripped:
            return False
        
        # 2. Только пробелы и знаки препинания
        if re.match(r'^[\s\.,!?\-_+=(){}[\]<>~`"\']*$', text_stripped):
            return False
        
        # 3. Только цифры и знаки
        if re.match(r'^[\d\s\.,!?\-_+=(){}[\]<>~`"\']*$', text_stripped):
            return False
        
        # ВСЕ ОСТАЛЬНОЕ АВТОМАТИЧЕСКИ ПРОХОДИТ!
        # Даже "да", "нет", "ок" - пусть пользователь сам решает
        return True
    
    @staticmethod
    def is_valid_for_processing(text):
        """УЛЬТРА-МЯГКАЯ валидация"""
        # Проверяем только длину
        length_valid, length_error = MessageValidator.validate_message_length(text)
        if not length_valid:
            return False, length_error
        
        # Минимальная проверка на осмысленность
        if not MessageValidator.has_potential_for_reformulation(text):
            return False, "not_toxic"
        
        return True, "valid"
    
    @staticmethod
    def clean_text(text):
        """Очистка текста от лишних символов"""
        text = re.sub(r'\s+', ' ', text.strip())
        return text

# Экземпляр валидатора
validator = MessageValidator()
