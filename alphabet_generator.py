from PIL import Image, ImageDraw, ImageFont
import imageio
import json

def generate_alphabet():
	font = ImageFont.truetype('Pillow/Tests/fonts/FreeMonoBold.ttf', 20)
	text = \
'''A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
a b c d e f g h i j k l m n o p q r s t u v w x y z'''

	image = Image.new('L', (630, 60), 255)
	ImageDraw.Draw(image).text((10,10), text, font=font, fill=0)

	imageio.imwrite('alphabet.jpg', image)


generate_alphabet()