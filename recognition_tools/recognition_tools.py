from PIL import Image, ImageDraw, ImageFont
import statistics
import json
import math

class ConfigValidationException(Exception):
    pass

def load_image(filename):
    return Image.open(filename).convert('L')

def get_dominant_color(image):
    '''
    Returns color of the most prevalent pixel of `image`
    '''
    return max(image.getcolors(image.size[0]*image.size[1]))[1]

def get_lines(image, ease):
    '''
    Separate `image` into text lines

    Args:
        image: input image.

    Returns:
        
    '''
    lines_images = []
    width, height = image.width, image.height
    print(width, height)

    image_flattened = list(image.getdata())
    mode = get_mode(image)
    dominant_color = get_dominant_color(image)
    # average_color = statistics.mean(image_flattened)
    # average_color = image.resize((1, 1)).getpixel((0, 0))
    # print(average_color)
    i = 0

    while i < height:
        while i < height and not in_text(dominant_color, image_flattened[i*width : (i+1)*width-1], mode, ease):
            # print(f'{i}: OUT ', statistics.mean(image_flattened[i*width : (i+1)*width-1]))
            i = i+1
        from_pixel_line = i
        while i < height and in_text(dominant_color, image_flattened[i*width : (i+1)*width-1], mode, ease):
            # print(f'{i}: IN  ', statistics.mean(image_flattened[i*width : (i+1)*width-1]))
            statistics.mean(image_flattened[i*width : (i+1)*width-1])
            i = i+1
        to_pixel_line = i-1
        print(0, from_pixel_line, (width-1), to_pixel_line)
        if from_pixel_line < to_pixel_line:
            lines_images.append(image.crop((0, from_pixel_line, (width-1), to_pixel_line)))
        i = i+1

    return lines_images

def get_letters(line, ease):
    '''
    Separate `line` into letters
    '''
    image = line.transpose(Image.TRANSPOSE)
    letters = get_lines(image, ease)

    return [letter.transpose(Image.TRANSPOSE) for letter in letters]

def in_text(dominant_color, row, mode, ease):
    if mode == 'positive':
        return statistics.mean(row) < dominant_color-ease
    if mode == 'negative':
        return statistics.mean(row) > dominant_color+ease

def get_mode(image):
    average_color = image.resize((1, 1)).getpixel((0, 0))
    dominant_color = get_dominant_color(image)
    if average_color < dominant_color:
        return 'positive'
    else:
        return 'negative'

def get_profiles(image, mode):
    width, height = image.width, image.height

    if mode == 'positive':
        image_flattened = list(image.getdata())
        profile_x = [sum(image_flattened[i*width : (i+1)*width-1]) / width for i in range(height)]

        image_flattened = list(image.transpose(Image.TRANSPOSE).getdata())
        profile_y = [sum(image_flattened[i*height : (i+1)*height-1]) / height for i in range(width)]
    
    if mode == 'negative':
        image_flattened = [255 - elem for elem in list(image.getdata())]
        profile_x = [sum(image_flattened[i*width : (i+1)*width-1]) / width for i in range(height)]
        
        image_flattened = [255 - elem for elem in list(image.transpose(Image.TRANSPOSE).getdata())]
        profile_y = [sum(image_flattened[i*height : (i+1)*height-1]) / height for i in range(width)]

    return profile_x, profile_y

def interpolate_profiles(left, right):
    len_left, len_right = len(left), len(right)

    if len_left == len_right:
        return left, right

    if len_left > len_right:
        base = right
        change = left
    else:
        base = left
        change = right
    
    new_profile = []
    for i, value in enumerate(change):
        if i == 0 or i == len(change)-1:
            new_profile.append(value)
            continue
        
        change_margin = i*(1/(len(change)-1))
        j=0
        # while change_margin

def get_profiles_distance(left, right):
    if len(left) != len(right):
        return None

    return [abs(left[i]-right[i])**2 for i in range(len(left))]

def simple_config_ok(data):
    for entry in data:
        if not ('filename' in entry and
                'output' in entry):
            return False
    return True
