from PIL import Image
from selenium import webdriver


class ImageCompare(object):

    def make_regalur_image(self, img, size=(256, 256)):
        return img.resize(size).convert('RGB')

    def split_image(self, img, part_size=(64, 64)):
        w, h = img.size
        pw, ph = part_size
        assert w % pw == h % ph == 0
        return [img.crop((i, j, i+pw, j+ph)).copy() for i in range(0, w, pw) for j in range(0, h, ph)]

    def hist_similar(self, lh, rh):
        '''
        统计分割后每部分图片的相似度频率曲线
        '''
        assert len(lh) == len(rh)
        return sum(1 - (0 if 1 == r else float(abs(1 - r)) / max(1, r)) for l, r in zip(lh, rh)) / len(lh)

    def calc_similar(self, li, ri):
        '''
        计算两张图片的相似度
        '''
        return sum(self.hist_similar(l.histogram(), r.histogram()) for l, r in zip(self.split_image(li), self.split_image(ri))) / 16.0

    def calc_similar_by_path(self, lf, rf):
        li, ri = self.make_regalur_image(Image.open(
            lf)), self.make_regalur_image(Image.open(rf))
        return self.calc_similar(li, ri)


ic = ImageCompare()


driver = webdriver.Firefox()
driver.get('http://www.sogou.com')
driver.save_screenshot('001.png')

driver.get('http://www.baidu.com')
driver.save_screenshot('002.png')

print(ic.calc_similar_by_path('001.png', '002.png') * 100)
