from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

font_size = 33
wrap_width = 25
line_thickness = 7
line_height_factor = 1.4
base_line_height = int(font_size * line_height_factor)
header_spacing = 30
margin = 32

def textsize(text, font):
    im = Image.new('P', (0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def draw_strike(draw, text, position, font, fill='black'):
    width, height = textsize(text, font)
    x, y = position
    line_y = y + height - font.getmetrics()[1]
    draw.text((x, y), text, font=font, fill=fill)
    draw.line((x, line_y, x + width, line_y), fill=fill, width=line_thickness)

def create_footer(draw, width, current_height=0):
    footer_text = [
        "xxxxxxxxxxxxxxxxxxxxxxxx",
        "------------------------"
       
    ]
    y_position = current_height + base_line_height
    footer_font = ImageFont.truetype("Roboto_Mono/RobotoMono-VariableFont_wght.ttf", font_size)
    footer_height = 0

    for text in footer_text:
        text_width, text_height = textsize(text, footer_font)
        x_position = margin  # Left align the text
        draw.text((x_position, y_position), text, font=footer_font, fill='black')
        y_position += (base_line_height - 20)
        footer_height += base_line_height

    return footer_height

from PIL import ImageFont, ImageDraw




def create_header(draw, width, date, user, via):
    header_text = [
        f"posted at {date}",
        f"by {user}",
        f"via {via}"
    ]
    header_speparator = [
        
        "------------------------",
        "xxxxxxxxxxxxxxxxxxxxxxxx" 
    ]
    y_position = header_spacing
    header_font = ImageFont.truetype("Roboto_Mono/RobotoMono-VariableFont_wght.ttf", font_size)
    header_height = 0

    for text in header_text:
        text_width, text_height = textsize(text, header_font)
        x_position = margin  # Left align the text
        draw.text((x_position, y_position), text, font=header_font, fill='black')
        y_position += base_line_height
        header_height += base_line_height


    for text in header_speparator:
        text_width, text_height = textsize(text, header_font)
        x_position = margin
        draw.text((x_position, y_position), text, font=header_font, fill='black')
        y_position += (base_line_height - 20)
        header_height += base_line_height

    return y_position, header_height

def create_receipt(text, count, date, user, via):
    dpi = 203
    width_mm = 76
    width = int(546)
    strikethrough_words = ['woman', 'female', 'women']
    processed_words = []
    for word in text.split():
        if any(subword in word.lower() for subword in strikethrough_words):
            processed_words.append(word + " HUMAN")
        else:
            processed_words.append(word)
    processed_text = ' '.join(processed_words)
    
    

    font = ImageFont.truetype("Roboto_Mono/RobotoMono-VariableFont_wght.ttf", font_size)
    lines = textwrap.wrap(processed_text, width=wrap_width)
    
    text_height = len(lines) * base_line_height

    image = Image.new('RGB', (width, 10), 'white')
    draw = ImageDraw.Draw(image)
    
    header_y_start, header_height = create_header(draw, width, date, user, via)
    footer_height = create_footer(draw, width)
    total_height = text_height + header_height + footer_height + 180
    
    image = Image.new('RGB', (width, total_height), 'white')
    draw = ImageDraw.Draw(image)
    
    y_text_start, _ = create_header(draw, width, date, user, via)
    y_text = y_text_start + 90
    for line in lines:
        x_text = margin
        words = line.split()
        for word in words:
            formatted_word = word
            word_width, word_height = textsize(formatted_word, font)
            if any(subword in formatted_word.lower() for subword in strikethrough_words):
                draw_strike(draw, formatted_word, (x_text, y_text), font)
            else:
                draw.text((x_text, y_text), formatted_word, font=font, fill='black')
            x_text += word_width + 5
        y_text += base_line_height

    footer_y_start = y_text + 30
    create_footer(draw, width, footer_y_start)
    image.save(f'output/receipt_{count}.jpg')

def main():
    if not os.path.exists('output'):
        os.makedirs('output')
    with open('input.txt', 'r') as file:
        text_lines = file.readlines()

    date = "21:38"
    user = "tonytigher4325"
    via = "/Incel | reddit"

    for count, line in enumerate(text_lines):
        create_receipt(line, count + 1, date, user, via)

if __name__ == "__main__":
    main()
