from openai import OpenAI
import re
from config import OPENAI_API_KEY, OPENAI_PROMPT_TEMPLATE

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def generate_assertive_variants(self, text):
        """Генерация 3 ассертивных вариантов переформулировки"""
        try:
            prompt = OPENAI_PROMPT_TEMPLATE.format(text=text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты эксперт по ассертивной коммуникации. Твоя задача - помочь людям выражать свои мысли конструктивно и без агрессии. Всегда предлагай именно 3 варианта переформулировки, используя 'Я-сообщения' и избегая обвинений."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            variants = self._parse_variants(content)
            
            if len(variants) < 3:
                # Если не удалось распарсить 3 варианта, попробуем еще раз
                variants = self._extract_variants_fallback(content)
            
            return variants[:3]  # Берем только первые 3 варианта
            
        except Exception as e:
            print(f"Ошибка при обращении к OpenAI: {e}")
            return None
    
    def _parse_variants(self, content):
        """Парсинг вариантов из ответа GPT"""
        variants = []
        
        # Пытаемся найти пронумерованные варианты
        pattern = r'^\s*(\d+)\.?\s*(.+?)(?=^\s*\d+\.|\Z)'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            variant = match[1].strip()
            if variant:
                variants.append(variant)
        
        return variants
    
    def _extract_variants_fallback(self, content):
        """Резервный способ извлечения вариантов"""
        # Разбиваем по строкам и ищем любые варианты
        lines = content.split('\n')
        variants = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Вариант', 'Ответ', 'Переформулировка')):
                # Убираем номера в начале строки
                line = re.sub(r'^\d+\.?\s*', '', line)
                if len(line) > 10:  # Минимальная длина варианта
                    variants.append(line)
        
        # Если все еще мало вариантов, разделим весь текст на части
        if len(variants) < 3:
            sentences = re.split(r'[.!?]+', content)
            variants = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        return variants[:3]
    
    def format_variants_message(self, variants):
        """Форматирование вариантов для отправки пользователю"""
        if not variants or len(variants) == 0:
            return "Извините, не удалось сгенерировать варианты переформулировки."
        
        message = "✨ Вот 3 ассертивных варианта переформулировки:\n\n"
        
        for i, variant in enumerate(variants, 1):
            message += f"**{i}.** {variant}\n\n"
        
        message += "Выберите наиболее подходящий вариант или укажите, что ни один не подошел:"
        
        return message

# Глобальный экземпляр сервиса
llm_service = LLMService()
