from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import pandas as pd
import time
import string
import random

font_size = 30
sub_font_size = 24
wrap_width = 28
line_thickness = 14
line_height_factor = 1.4
base_line_height = int(font_size * line_height_factor)
header_spacing = 30
margin = 28
font = ImageFont.truetype("Gochi_Hand,IBM_Plex_Mono,Roboto,Roboto_Mono,Space_Mono/IBM_Plex_Mono/IBMPlexMono-Light.ttf", font_size)
subFont = ImageFont.truetype("Gochi_Hand,IBM_Plex_Mono,Roboto,Roboto_Mono,Space_Mono/IBM_Plex_Mono/IBMPlexMono-Light.ttf", sub_font_size)
boldFont = ImageFont.truetype("Gochi_Hand,IBM_Plex_Mono,Roboto,Roboto_Mono,Space_Mono/IBM_Plex_Mono/IBMPlexMono-Bold.ttf", font_size)

def textsize(text, font):
    im = Image.new('P', (0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

# def draw_strike(draw, text, position, font, fill='black'):
#     width, height = textsize(text, font)
#     x, y = position
#     #line_y = y + height - font.getmetrics()[1]
#     line_y = y  + 26
#     draw.text((x, y), text, font=font, fill=fill)
#     draw.line((x, line_y, x + width, line_y), fill=fill, width=line_thickness)

def draw_strike(draw, text, position, font, fill='black', brush_path='brush_medium.png'):
    # Assuming the 'font' is an ImageFont object instantiated outside this function
    # Load the brush image
    brush = Image.open(brush_path).convert("RGBA")
    brush_width, brush_height = brush.size

    # Calculate text size and line position using the correct method
    width, height = textsize(text, font)  # Adjust width to prevent overlap
    x, y = position
    line_y = y + 26  # Adjust based on your actual application needs
    
    # Draw text
    draw.text((x, y), text, font=font, fill=fill)
    max_line_length = width * 0.75  
    # Draw line using brush
    for i in range(0, int(min(width, max_line_length)), brush_width - 15):
      # Adjust spacing to prevent gaps
        # Randomness in brush position (you can adjust these values)
        offset_y = line_y + random.randint(-2, 2)  # Vertical variation
        rotation_angle = random.randint(-3, 3)     # Rotation variation
        
        # Rotate and reposition brush
        rotated_brush = brush.rotate(rotation_angle, expand=True)
        brush_stamp_x = x + i
        brush_stamp_y = offset_y - rotated_brush.size[1] // 2
        
        # Apply brush stamp
        draw.bitmap((brush_stamp_x, brush_stamp_y), rotated_brush, fill=fill)


def create_footer(draw, width, current_height=0):
    footer_text = [
        "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "---------------------------"
       
    ]
    y_position = current_height + base_line_height
    #font = ImageFont.truetype("Roboto_Mono/RobotoMono-VariableFont_wght.ttf", font_size)
    footer_height = 0

    for text in footer_text:
        text_width, text_height = textsize(text, font)
        x_position = margin  # Left align the text
        draw.text((x_position, y_position), text, font=font, fill='black')
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
    header_separator = [
        "---------------------------",
        "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ]
    y_position = header_spacing
    header_height = 0

    for i, text in enumerate(header_text):
        # Check if this is the 'user' line and split it
        if 'by' in text:
            prefix_text = "by "
            user_text = user
            # Calculate the position for the 'by' prefix
            prefix_width, prefix_height = textsize(prefix_text, font=font)
            draw.text((margin, y_position), prefix_text, font=font, fill='black')
            # Calculate the position for the 'user' text
            user_x_position = margin + prefix_width
            draw.text((user_x_position, y_position), user_text, font=boldFont, fill='black')
            # Update the text width for height calculation
            text_width, text_height = prefix_width + textsize(user_text, font=boldFont)[0], prefix_height
        else:
            # Use regular font for other lines
            text_font = font
            if text.startswith("via"):
                text_font = subFont
            text_width, text_height = textsize(text, font=text_font)
            draw.text((margin, y_position), text, font=text_font, fill='black')

        # Update y_position and header_height for the next text item
        y_position += base_line_height
        header_height += base_line_height


    for text in header_separator:
        text_width, text_height = textsize(text, font)
        x_position = margin
        draw.text((x_position, y_position), text, font=font, fill='black')
        y_position += (base_line_height - 20)
        header_height += base_line_height

    return y_position, header_height

replacement_dict = {
    'woman': '*man',
    'women': '*men',
    'girl': '*boy',
    'girls': '*boys',
    'female': '*male',
    'females': '*males',
    'masculine': '*feminine',
    'feminine': '*masculine',
    'androcentric': '*androphobic',
    'androcracy': '*fendrocracy',
    'gf': '*bf',
    'chad': '*girl',
    "chad's": "*girl's",
    "chads": "*girls",
    'simps': '*incels',
    'nigger': '*incel',
    'jew': '*incel',
    'jews': '*incels',
    'niggers': '*incels',
    'whores': '*male-prostitutes',
    'foids': '*incels',
    'foid': '*incel',
    'her': '*his',
    'his': '*her',
    'cunt': '*dick',
    'pussy': '*dick',
    'dick': '*pussy',
    'pussies': '*dicks',
    'men': '*women',
    'she': '*he',
    'males': '*women',
    'liberal': '*fascist'
}

def remove_punctuation_for_lookup(word):
    # Strip punctuation at the start and end of the word for lookup purposes
    return word.strip(string.punctuation)

def create_receipt(text, count, date, user, via):
    dpi = 203
    width_mm = 76
    width = int(546)
    strikethrough_words = list(replacement_dict.keys())
    
    # processed_words = []
    # for word in text.split():
    #     if any(subword in word.lower() for subword in strikethrough_words):
    #         processed_words.append(word + " HUMAN")
    #     else:
    #         processed_words.append(word)
    # processed_text = ' '.join(processed_words)
    
    processed_words = []
    for word in text.split():
        # Remove punctuation for the dictionary lookup
        lookup_word = remove_punctuation_for_lookup(word).lower()
        # Check if the cleaned lowercase word is in the dictionary
        if lookup_word in replacement_dict:
            # Keep the original word and append the replacement word
            processed_words.append(word + "  " + replacement_dict[lookup_word])
        else:
            # Append the original word if no replacement is found
            processed_words.append(word)
    # Join all processed words back into a single string
    processed_text = ' '.join(processed_words)

      

  
    lines = textwrap.wrap(processed_text, width=wrap_width)
    
    text_height = len(lines) * base_line_height

    image = Image.new('RGB', (width, 10), 'white')
    image = image.convert("P", palette=Image.ADAPTIVE, colors=32)

    # create a new image in index color mode

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
            # Check if the word starts with an asterisk and remove the asterisk if it does
            if word.startswith("*"):
                formatted_word = word[1:]  # Remove the leading asterisk
                current_font = boldFont  # Use the bold font
                apply_strikethrough = False
            else:
                formatted_word = word
                current_font = font  # Use the regular font
                apply_strikethrough = True

            # Remove punctuation for the purpose of strikethrough matching
            lookup_word = remove_punctuation_for_lookup(formatted_word).lower()

            # Get the size of the word to calculate the placement
            word_width, word_height = textsize(formatted_word, current_font)

            # Apply strikethrough only if it doesn't start with an asterisk and the word matches strikethrough words exactly
            if apply_strikethrough and lookup_word in strikethrough_words:
                draw_strike(draw, formatted_word, (x_text, y_text), current_font)
                # check if the word contains any https:// or http:// and if so strikethrough it
            else:
                if "http://" in formatted_word or "https://" in formatted_word:
                    draw_strike(draw, formatted_word, (x_text, y_text), current_font)
                # Draw the text using the selected font
                draw.text((x_text, y_text), formatted_word, font=current_font, fill='black')

            x_text += word_width + 15
        y_text += base_line_height


    footer_y_start = y_text + 30
    create_footer(draw, width, footer_y_start)

    image.save(f'output/receipt_{count}.png', "PNG")


def main():
    if not os.path.exists('output'):
        os.makedirs('output')

    df = pd.read_csv('incel.csv')
    for i in range(len(df)):
        # delay one second for each receipt
        #time.sleep(1)
        time_now = time.strftime('%H:%M')
        create_receipt(df['post'][i], i+1, time_now, df['user'][i], '/Incel | reddit')
if __name__ == "__main__":
    main()
