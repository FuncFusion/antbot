
# # Load a color emoji font
# font = ImageFont.truetype("noto_bold.ttf", size=60, layout_engine=ImageFont.Layout.BASIC)

# # Create image
# img = Image.new("RGBA", (400, 150), (30, 30, 30))
# draw = ImageDraw.Draw(img)

# # Draw colored emoji
# draw.text((20, 20), "Hello 😄🌍👍", font=font, fill=(255, 255, 255), embedded_color=True)

# # Save output
# img.show()
import aggdraw
from PIL import Image, ImageDraw, ImageFont

# Создаем холст
width, height = 400, 100
image = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # прозрачный фон

# Создаем рисовальщик aggdraw
draw = ImageDraw.Draw(image)

# Загружаем шрифт (путь к ttf и размер)
font_path = "merged_with_color.ttf"
# font_path = "C:/Windows/Fonts/arial.ttf"  # для Windows

font_size = 48
font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.Layout.RAQM)

# Пишем текст в центре холста
text = "Arial✨👆👆💩🧭"
text_position = (10, 10)
draw.text(text_position, text, font=font, embedded_color=True,)# fill=(255,255,255, 255))

image.show()

