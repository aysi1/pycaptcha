from PIL import Image, ImageFont, ImageDraw
from random import randint
from io import BytesIO
import base64
import time

from Crypto.Hash import SHA256, HMAC

IMAGE_WIDTH, IMAGE_HEIGHT = 120, 70

HMAC_KEY = b'my-captcha-key-100000000000182787828'

def generate_captcha():
    image = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('font/NerkoOne-Regular.ttf', 60)
    code = str(randint(1000, 9999))
    draw.text((10, 0), code, (0, 0, 0), font=font)
    colors = ['red', 'dodgerblue', '#FB2576', '#3F0071']
    y = 10
    for i in range(3):
        y += randint(20, 30)
        draw.line([(randint(0, 10), y), (100, IMAGE_HEIGHT - y)], colors[i], 4)

    draw.line([(IMAGE_WIDTH // 2, y), (120, 0)], colors[3], 3)
    io = BytesIO()
    image.save(io, format='PNG')
    b64 = 'data:image/png;base64,' + base64.b64encode(io.getbuffer()).decode()

    ts = str(int(time.time())).encode()
    code = code.encode()
    h = SHA256.new(b64.encode()).hexdigest().encode()
    sig = HMAC.new(HMAC_KEY, h + b':' + ts + b':' + code, digestmod=SHA256).hexdigest()
    return (b64, h.decode(), ts.decode(), sig)


def verify_captcha_answer(h, ts, sig, answer):
    try:
        if time.time() - ts > 60 * 10: # the captcha stays valid for 10 minutes only
            return False
        HMAC.new(HMAC_KEY, h.encode() + b':' + ts.encode() + b':' + answer.encode(), digestmod=SHA256).hexverify(sig)
        return True
    except Exception:
        return False


img, h, ts, sig = generate_captcha()

# print(h, ts, sig)

with open('txt.txt', 'w') as fp:
    fp.write(img)


code = input('captcha: ')

if verify_captcha_answer(h, ts, sig, code):
    print('solved!')
else:
    print('uh oh')