"""
@Auther:Noah Miller
@Date: 2024/8/1
@Blog: https://blog.csdn.net/weixin_54444518
@灵感来源:
   - @Author: 偶尔有点小迷糊(Bilibili)
   - @link:【『整活』用百万汉字拼一张彩色照片】 https://www.bilibili.com/video/BV1mq4y1n7aE/?share_source=copy_web&vd_source=136849b7b9a5d8445987a371deb2fbf9
"""

LIB_MISSING = "缺失关键库, 正在安装(但一定要有Pip)..."
INSTALL_SUCCESSED = "安装完成"
PROCESSED_AND_SAVING = "图片处理完成, 正在保存..."

# 保Pillow, Click导入
import os
try:
    from PIL import Image, ImageDraw, ImageFont
    import click
except ImportError:
    print(LIB_MISSING)
    os.system("python -m ensurepip")
    os.system("python -m pip install --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple/")
    os.system("pip install pillow  -i https://pypi.mirrors.ustc.edu.cn/simple/")
    os.system("pip install click  -i https://pypi.mirrors.ustc.edu.cn/simple/")
    print(INSTALL_SUCCESSED)
    from PIL import Image, ImageDraw, ImageFont
    import click


# 参数设置
class Setting:
    chunkHeight = chunkWidth = 16               # 拼图块尺寸
    fontSize = 16                               # 字体大小
    imageMode = "RGBA"                          # 图像模式

    fontRelPath = "./AliPuHui-Bold.ttf"         # 字体文件相对路径
    f = open(fontRelPath, "rb")                 # 下面连着三步是为了能正常创建字体对象, 如果这样依旧报错, 把字体路径改成绝对路径
    font = ImageFont.truetype(f, fontSize)                
    f.close()

    chunkFill = "lightgrey"                     # 拼图块背景填充颜色, 亮灰色效果可以
    chunkOutline = None                         # 拼图块边框, 一般测试的时候用, 可以把拼图框架网格化
    chunkOutlineWidth = 1                       # 拼图块边框宽度

setting = Setting()


# 用(已经绑定拼图块图片对象的)ImageDraw对象绘制拼图块
def drawChar2ChunkByImageDrawObj(char, draw:ImageDraw.ImageDraw, offsetX:int, offsetY:int, fill, outline, color):
    draw.rectangle(
        (0, 0, setting.chunkWidth, setting.chunkHeight),
        fill=color,
        outline=outline,
        width=setting.chunkOutlineWidth,
    )
    # 渲染文字, anchor特别重要,它指定了对其方式|anchor文档传送门: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors  
    draw.text((offsetX, offsetY), char, font=setting.font, fill=fill, anchor="mm")






# 组织各函数进行图片文字化的函数




@click.command()
@click.argument("fp",type=click.Path(exists=True))
@click.argument("text")
@click.option("-c", "--color", default=setting.chunkFill, help="指定拼图块背景颜色")
@click.option("-l", "--outline-color", default=setting.chunkOutline, help="指定拼图块边框颜色.")
@click.option("-o", "--output",default="output.png", help="指定文件输出路径")
@click.option("-h", "--height", default=setting.chunkHeight, help="指定拼图块高度")
@click.option("-w", "--width", default=setting.chunkWidth, help="指定拼图块宽度")
@click.option("-m", "--mode", default=setting.imageMode, help="指定图片模式")
@click.option( "-fs", "--font-size", default=setting.fontSize, help="指定字体大小")
@click.option("-ff", "--font-family", default=setting.fontRelPath, help="指定字体")
def process(text, fp, mode, width, height,output, outline_color, color, font_size, font_family):
    imgSrc = Image.open(fp)                     # 加载原图
    w, h = imgSrc.size                          # 原图尺寸
    # 创建拼图块的图片对象
    chunk = Image.new(mode, (width, height))

    # 创建拼图框架的图片对象
    picFrame = Image.new(mode, (width*w, height*h))

    # 创建ImageDraw对象并绑定拼图块图片对象
    draw = ImageDraw.Draw(chunk, mode)
    charIndex = 0                               # 待渲染的字符在text序列里的索引

    for y in range(h):
        print(f"正在处理第{y+1}行, 还剩{h-y-1}行未处理.")
        for x in range(w):
            # 绘制拼图块
            drawChar2ChunkByImageDrawObj(
                text[charIndex],
                draw,
                width/2,
                height/2,
                fill=imgSrc.getpixel((x,y)),
                color=color,
                outline=outline_color,
            )

            # 拼图块拼到拼图框架的合适位置 (粘贴到指定位置)
            picFrame.paste(chunk, (x*setting.chunkWidth, y*setting.chunkHeight))

            charIndex+=1
            if charIndex == len(text):
                charIndex = 0
    print(PROCESSED_AND_SAVING)
    picFrame.save(output)
    print(f"图片已保存至 '{os.path.abspath(output)}'")


if __name__ == "__main__":
    process()

