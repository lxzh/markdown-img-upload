# coding: utf-8
from clipboard import get_paste_img_file
from upload import upload_img
import util
import os
import subprocess
import sys
import time

if not os.path.exists(util.CONFIG_FILE):
    util.generate_config_file()

config = util.read_config()
if not config:
    name = util.picbed_name()
    util.notice('请先设置你的%s信息'%name)
    util.open_with_editor(util.CONFIG_FILE)
    sys.exit(0)

url = '%s/%s' % (config['url'], config['prefix'])

result = get_paste_img_file()
if result:
    img_file, need_format, format = result
    # has image

    # use time to generate a unique upload_file name, we can not use the tmp file name
    upload_name = "%s.%s" % (int(time.time() * 1000), format)
    if need_format:
        size_str = subprocess.check_output('sips -g pixelWidth %s | tail -n1 | cut -d" " -f4' % img_file.name, shell=True)
        size = int(size_str.strip()) / 2
        markdown_url = '<img src="%s/%s" width="%d"/>' % (url, upload_name, size)
    else:
        markdown_url = '%s/%s' % (url, upload_name)

    # make it to clipboard
    os.system("echo '%s' | pbcopy" % markdown_url)
    #os.system('osascript -e \'tell application "System Events" to keystroke "v" using command down\'')
    upload_file = util.try_compress_png(img_file, format!='gif')
    if upload_img(upload_file.name, upload_name): util.notice("上传图片到图床成功")
    else: util.notice("上传图片到图床失败，请检查网络后重试")
else:
    util.notice("剪切版里没有图片！")

    # imagefilename = "/tmp/1486878546367.png"
    #upload_img(imagefilename, '12345.png')