import re
import mojimoji


def title_convert(title):
    code_regex = re.compile('[ 　!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~〜＝＋「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％･・]')
    
    title = str(title)

    # カタカナ、数字、英語を全て半角へ変換
    cleaned_title1 = mojimoji.zen_to_han(title)

    # 特殊文字、空白等削除
    cleaned_title2 = code_regex.sub('', cleaned_title1) 

    # アルファベットを全て小文字へ変換
    cleaned_title3 = cleaned_title2.lower()

    return cleaned_title3

