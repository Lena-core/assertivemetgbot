import urllib.parse

# Test basic URL encoding
text = "Hello world test"
encoded = urllib.parse.quote(text)
print("Original:", text)
print("Encoded:", encoded)
print("URL:", f"tg://msg?text={encoded}")
