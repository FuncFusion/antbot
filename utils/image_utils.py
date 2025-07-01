from PIL import Image, ImageDraw, ImageFont, ImageSequence
from io import BytesIO
from typing import Callable


def edit_image(image: Image.Image, extension: str, edit_func: Callable[..., Image.Image], **kwargs):
    byteslike = BytesIO()

    # NO JPEGs ALLOWED
    if extension.lower() in ("jpeg", "jpg"):
        extension = "PNG"
        image = image.convert(mode="RGBA")

    if not getattr(image, 'is_animated', False):
        edited = edit_func(image, **kwargs)
        edited.save(byteslike, format=extension)

    else:
        frames: list[Image.Image] = []
        durations = []
        for frame in ImageSequence.Iterator(image):
            edited_frame = edit_func(frame, **kwargs)
            frames.append(edited_frame)
            durations.append(frame.info.get("duration", 40))

        frames[0].save(
            byteslike,
            format=extension.upper(),
            save_all=True,
            optimize=False,
            append_images=frames[1:],
            duration=durations,
            disposal=2,
            loop=image.info.get('loop', 0)
        )

    byteslike.seek(0)
    return byteslike


class ImageText(object):
    def __init__(self, image, mode='RGBA', anchor="la", stroke_width=0, stroke_fill=None):
        self.image = image
        self.size = self.image.size
        self.draw = ImageDraw.Draw(self.image)
        self.anchor = anchor
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_path, font_size=11,
               color=(0, 0, 0), max_width=None, max_height=None):
        x, y = xy
        if font_size == 'fill':
            font_size = self.get_font_size(text, font_path, max_width, max_height)
        
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.Layout.RAQM)
        text_size = self.get_text_size(font_path, font_size, text)
    
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
    
        self.draw.text((x, y), text, font=font, fill=color, anchor=self.anchor, 
                       stroke_width=self.stroke_width, stroke_fill=self.stroke_fill, embedded_color=True)
        return text_size

    def get_text_size(self, font_path, font_size, text):
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.Layout.RAQM)
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]


    def write_text_box(self, xy, text, box_width, font_path,
           font_size=11, color=(0, 0, 0), stroke_width=0, 
           stroke_fill=None, place='left', justify_last_line=False
        ):
        x, y = xy
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.Layout.RAQM)
        words = text.split()
        lines = []
        current_line = []
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill
        
        for word in words:
            # Handle words that are longer than box_width
            if self.get_text_size(font_path, font_size, word)[0] > box_width:
                # If we have words in current_line, add them as a line first
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                
                # Split long word
                remaining_word = word
                while remaining_word:
                    # Try to fit as much of the word as possible
                    for i in range(len(remaining_word), 0, -1):
                        part = remaining_word[:i]
                        if self.get_text_size(font_path, font_size, part)[0] <= box_width:
                            lines.append(part)
                            remaining_word = remaining_word[i:]
                            break
                    # If we couldn't fit even one character, force split at first char
                    if len(remaining_word) == len(word):
                        lines.append(remaining_word[0])
                        remaining_word = remaining_word[1:]
                continue
                
            # Test if adding this word exceeds the box width
            test_line = ' '.join(current_line + [word])
            test_width = self.get_text_size(font_path, font_size, test_line)[0]
            
            if test_width <= box_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line if there are remaining words
        if current_line:
            lines.append(' '.join(current_line))
    
        # Get line metrics from a sample line containing ascenders and descenders
        sample_text = "ÁjpqÜ"  # Text with both ascenders and descenders
        line_height = self.get_text_size(font_path, font_size, sample_text)[1]
        fixed_spacing = int(line_height * 1.2)  # 20% extra space
        
        for index, line in enumerate(lines):
            text_width = self.get_text_size(font_path, font_size, line)[0]
            current_y = y + (fixed_spacing * index)
            
            if place == 'left':
                self.write_text((x, current_y), line, font_path, font_size, color)
            elif place == 'right':
                x_left = x + box_width - text_width
                self.write_text((x_left, current_y), line, font_path, font_size, color)
            elif place == 'center':
                x_left = int(x + ((box_width - text_width) / 2))
                self.write_text((x_left, current_y), line, font_path, font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or len(words) == 1:
                    self.write_text((x, current_y), line, font_path, font_size, color)
                    continue
                total_size = self.get_text_size(font_path, font_size, ''.join(words))
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text((start_x, current_y), word, font_path, font_size, color)
                    word_size = self.get_text_size(font_path, font_size, word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_path, font_size, words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text((last_word_x, current_y), words[-1], font_path, font_size, color)
        
        total_height = y + (fixed_spacing * (len(lines) - 1)) + line_height
        return (box_width, total_height - y)

    def get_height(self, xy, text, box_width, font_path,
           font_size=11, color=(0, 0, 0), place='left', stroke_width=0, stroke_fill=None,
           justify_last_line=False):
        x, y = xy
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.Layout.RAQM)
        words = text.split()
        lines = []
        current_line = []
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill
        
        for word in words:
            # Handle words that are longer than box_width
            if self.get_text_size(font_path, font_size, word)[0] > box_width:
                # If we have words in current_line, add them as a line first
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                
                # Split long word
                remaining_word = word
                while remaining_word:
                    # Try to fit as much of the word as possible
                    for i in range(len(remaining_word), 0, -1):
                        part = remaining_word[:i]
                        if self.get_text_size(font_path, font_size, part)[0] <= box_width:
                            lines.append(part)
                            remaining_word = remaining_word[i:]
                            break
                    # If we couldn't fit even one character, force split at first char
                    if len(remaining_word) == len(word):
                        lines.append(remaining_word[0])
                        remaining_word = remaining_word[1:]
                continue
                
            # Test if adding this word exceeds the box width
            test_line = ' '.join(current_line + [word])
            test_width = self.get_text_size(font_path, font_size, test_line)[0]
            
            if test_width <= box_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line if there are remaining words
        if current_line:
            lines.append(' '.join(current_line))
    
        # Get line metrics from a sample line containing ascenders and descenders
        sample_text = "Ёjp"  # Text with both ascenders and descenders
        line_height = self.get_text_size(font_path, font_size, sample_text)[1]
        fixed_spacing = int(line_height * 1.2)  # 20% extra space
        total_height = y + (fixed_spacing * (len(lines) - 1)) + line_height
        return total_height - y

