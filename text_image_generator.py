from PIL import Image, ImageDraw, ImageFont
import imageio
import json

def generate_lorem_ipsum():
	font = ImageFont.truetype('Pillow/Tests/fonts/FreeMonoBold.ttf', 20)
	text = \
'''Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod, tempor incididunt ut labore et dolore,
magna aliqua. Ut enim ad minim veniam, quis nostrud
exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit
in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.'''


	hues = [ min(int(i*256/16), 255) for i in range(17) ]
	config = []

	for bg_hue in hues:
		for text_hue in [hue for hue in hues if abs(bg_hue - hue) >= 31]:
			image = Image.new('L', (760, 180), (bg_hue))
			ImageDraw.Draw(image).text((10,10), text, font=font, fill=(text_hue))

			filename = f'./generated_examples/{bg_hue:03}-{text_hue:03}.jpg'
			imageio.imwrite(filename, image)
			config.append({
				'filename': filename,
				# 'mode': 'negative' if text_hue > bg_hue else 'positive',
				'output': f'./generated_examples_output/{bg_hue:03}-{text_hue:03}-{{}}.jpg',
				'folder': f'./generated_examples_output/{bg_hue:03}-{text_hue:03}'
			})
			# image.show()
		print([hue for hue in hues if abs(bg_hue - hue) >= 31])

	with open('config2.json', 'w') as outfile:
		outfile.write(json.dumps(
			config,
			indent=4,
			separators=(',', ': ')
		))

generate_lorem_ipsum()