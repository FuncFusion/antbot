# from PIL import Image, ImageDraw, ImageFont

# # Load a color emoji font
# font = ImageFont.truetype("noto_bold.ttf", size=60, layout_engine=ImageFont.Layout.BASIC)

# # Create image
# img = Image.new("RGBA", (400, 150), (30, 30, 30))
# draw = ImageDraw.Draw(img)

# # Draw colored emoji
# draw.text((20, 20), "Hello 😄🌍👍", font=font, fill=(255, 255, 255), embedded_color=True)

# # Save output
# img.show()
from PIL import Image
import aggdraw

# Создаем холст
width, height = 400, 100
image = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # прозрачный фон

# Создаем рисовальщик aggdraw
draw = aggdraw.Draw(image)

# Загружаем шрифт (путь к ttf и размер)
font_path = r"C:\Users\bth123\_coding\antbot\assets\memes\noto_bold.ttf"
font_path = "C:/Windows/Fonts/arial.ttf"  # для Windows

font_size = 48
font = aggdraw.Font("black", font_path, font_size)

# Пишем текст в центре холста
text = "Hello 😊 Emojis!"
text_position = (10, 10)
draw.text(text_position, text, font)

# Финализируем рисунок
draw.flush()

# Сохраняем результат
image.show()
