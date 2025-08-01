# 🧪 Инструкция по тестированию функциональности v2.1

## 🚀 Как протестировать улучшения

### 1. Запуск стабильной версии бота
```bash
cd C:\Projects\assertivemetgbot
venv\Scripts\activate
python main_simple_stable.py
```

### 2. Базовый тестовый сценарий

#### Шаг 1: Отправьте токсичное сообщение
Примеры текстов для тестирования:
- "Ты совсем дурак, ничего не понимаешь!"
- "Это полная чушь, автор идиот"
- "Надоели уже эти тупые вопросы"

#### Шаг 2: Получите 3 варианта
Бот должен сгенерировать и показать 3 ассертивных варианта с кнопками:
- [Выбрать 1]
- [Выбрать 2]  
- [Выбрать 3]
- [Ни один не подошел]

**ОБРАТИТЕ ВНИМАНИЕ:** кнопка "⭐ Поддержать проект" НЕ должна появляться в основном меню!

#### Шаг 3: Выберите любой вариант (1, 2 или 3)
После выбора должны появиться кнопки:
- [✉️ Переслать в любой чат]
- [🤖 Поделиться ботом]
- **[⭐ Поддержать проект]** ← НОВАЯ КНОПКА

### 3. Тестирование обычных функций

**✉️ Переслать в любой чат:**
- Должна открыться Telegram с полем ввода
- В поле должен быть предзаполнен выбранный текст
- Можно выбрать любой чат для отправки

**🤖 Поделиться ботом:**
- Должна открыться форма шеринга
- В сообщении должна быть ссылка на бота и описание

### 4. 🆕 Тестирование донатов ⭐

#### Сценарий A: Донат после выбора варианта (ОСНОВНОЙ)
1. Отправьте токсичное сообщение: "Ты полный дурак!"
2. Получите 3 варианта с кнопками выбора (БЕЗ кнопки доната!)
3. **Выберите любой вариант (1, 2 или 3)**
4. В меню действий найдите "⭐ Поддержать проект"
5. Нажмите на неё
6. Выберите "1 ⭐ Звезда" или "5 ⭐ Звёзд"
7. Должен появиться инвойс Telegram Stars
8. Пройдите процедуру оплаты (в тестовом режиме)
9. Получите сообщение благодарности

#### Сценарий B: Прямой донат по команде
1. Отправьте `/donate`
2. Должны появиться варианты доната
3. Завершите процесс оплаты

#### ❌ Сценарий C: "Ни один не подошел" (БЕЗ доната)
1. Выберите "Ни один не подошел"
2. **Кнопка доната НЕ должна появиться**
3. Только запрос причины отказа

### 5. Тестирование "Ни один не подошел"

#### Шаг 1: Нажмите "Ни один не подошел"
Бот должен запросить причину:
"Жаль, что ничего не подошло. Не могли бы вы кратко объяснить почему?"

#### Шаг 2: Отправьте причину
Примеры: "непонятно", "слишком формально", "не по смыслу"

#### Шаг 3: Получите благодарность
Бот должен поблагодарить: "Спасибо за ваш выбор!"

## 🔍 Что проверить

### ✅ Функциональные тесты
- [ ] Генерация 3 вариантов работает
- [ ] Кнопки выбора вариантов работают
- [ ] ✅ Кнопка доната НЕ появляется в основном меню
- [ ] ✅ Кнопка доната появляется после выбора варианта (1, 2, 3)
- [ ] ❌ Кнопка доната НЕ появляется при "Ни один не подошел"
- [ ] ⭐ Команда `/donate` работает
- [ ] ⭐ Варианты доната (1 и 5 звёзд) отображаются
- [ ] ⭐ Инвойс Telegram Stars создается
- [ ] ⭐ Сообщение благодарности отправляется после оплаты
- [ ] URL-ссылки корректно открываются в Telegram
- [ ] Текст корректно предзаполняется в поле ввода
- [ ] Обратная связь "Ни один не подошел" работает
- [ ] Сбор метрик в базу данных работает

### ✅ UI/UX тесты  
- [ ] Сообщения красиво форматированы
- [ ] Выбранный текст выделен курсивом
- [ ] Emoji в кнопках отображаются
- [ ] ⭐ Кнопка доната не мешает основному функционалу
- [ ] ⭐ Сообщения о донате мотивируют пользователя
- [ ] Благодарственное сообщение мотивирует
- [ ] Кнопка шеринга призывает поделиться ботом

### ✅ Технические тесты
- [ ] Кириллические символы корректно кодируются в URL
- [ ] Спецсимволы и emoji обрабатываются правильно
- [ ] Длинные тексты корректно кодируются
- [ ] ⭐ Pre-checkout query обрабатывается
- [ ] ⭐ Successful payment обрабатывается
- [ ] ⭐ Логи донатов записываются
- [ ] Нет ошибок в логах при работе с URL и платежами

## 🐛 Что делать при ошибках

### Ошибка: "Запрос не найден"
- Проверьте, что user_requests содержит данные пользователя
- Убедитесь, что структура {'request_id': ..., 'variants': ...} корректна

### Ошибка: Кнопки не работают
- Проверьте URL-энкодинг текста
- Убедитесь, что используется правильный формат tg://msg?text=...

### ⭐ Ошибка: Донат не работает
- Проверьте, что бот поддерживает Telegram Stars
- Убедитесь, что provider_token пустой для XTR валюты
- Проверьте обработку pre_checkout_query

### Ошибка: Плохое форматирование
- Проверьте parse_mode='Markdown' в сообщениях
- Убедитесь, что спецсимволы экранированы

## 📊 Проверка метрик

Запустите для проверки сохранения данных:
```bash
python stats.py
```

Должны увидеть:
- Количество уникальных пользователей
- Статистику выбора вариантов (1, 2, 3)
- Причины отказов от вариантов

## 🎯 Критерии успешного тестирования

Тест считается пройденным, если:
1. ✅ Все кнопки работают без ошибок
2. ✅ URL корректно открываются в Telegram  
3. ✅ Текст предзаполняется в поле ввода
4. ✅ Кнопка доната НЕ появляется в основном меню
5. ✅ Кнопка доната появляется после выбора варианта
6. ❌ Кнопка доната НЕ появляется при "Ни один не подошел"
7. ⭐ Процесс доната работает end-to-end
8. ⭐ Сообщение благодарности отправляется
9. ✅ Метрики сохраняются в базу данных
10. ✅ Нет ошибок в логах бота
11. ✅ Пользователь может легко скопировать и отправить текст
12. ✅ Шеринг бота работает корректно

## 🎉 Ожидаемый результат

После тестирования пользователь должен иметь полный опыт:
1. Получить качественные ассертивные варианты
2. Легко отправить выбранный текст в любой чат
3. При желании поддержать проект донатом
4. Поделиться ботом с друзьями

**Все функции должны работать гладко и интуитивно!** 🚀

## 📞 Поддержка

При проблемах с тестированием:
1. Проверьте логи: они покажут ошибки в деталях
2. Запустите простые тесты для проверки базового функционала
3. Убедитесь, что .env файл содержит корректные токены
4. Проверьте интернет-соединение и доступность OpenAI API
5. ⭐ Для тестирования донатов убедитесь, что у бота есть права на Telegram Stars
