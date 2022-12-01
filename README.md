# pycaptcha
Simple Python captcha library


> Example with Flask

```python

@app.route('/generate')
def generate():
  img, h, ts, sig = generate_captcha()
  # img: base64 encoded image
  return jsonify(dict(img=img, timestamp=ts, h=h, sig=sig))

@app.route('/verify', methods=['POST'])
def verify():
  res = request.get_json()
  h = res.get('h')
  ts = res.get('ts')
  sig = res.get('sig')
  answer = res.get('answer')
  return {'valid': verify_captcha_answer(h, ts, sig, answer)}

```
