from PIL import Image

import wrapper

"""
not support compress format (ex. jpg/jpeg)

test case: http://captcha.naver.com/nhncaptchav4.gif

"""

f = wrapper.extract_file_by_url('http://captcha.naver.com/nhncaptchav4.gif')
print wrapper.bypass_captcha_from_file(f)  # original
print wrapper.bypass_captcha_from_file(f, monochrome=True)  # monochrome
print wrapper.bypass_captcha_from_file2(f)  # split
im = Image.open(f)
im.show()
