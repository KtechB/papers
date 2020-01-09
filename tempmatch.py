import sys,os

import matplotlib.pyplot as plt
import math
import numpy as np
import cv2
# import re
# from glob import glob
# from ngram import NGram
# import time
import pickle
import itertools
import operator
# import collections

## 様々な条件でaffine変換とtemplate matchingを行い、最善の結果を返す
## 様々な条件でaffine変換とtemplate matchingを行い、最善の結果を返す(CORR or COEF用)
class Affined_temp_match():
    ## 回転角度
    theta_space = np.linspace(-0.2, 0.2, num=3)/180.0*np.pi
    #theta_space = np.linspace(-0.5, 0.5, num=41)/180.0*np.pi

    ## 縮尺
#     pct_lambda_space = np.linspace(1.95, 2.05, num=21)
    pct_lambda_space = np.array([1.0])

    ## 回転行列
    rotation_matrices = []

    ## padding size
    # scan_image(draft_image)に対して周囲に何pxのパディングを行い、かつ、
    # RIP_image(product_image)の周囲何pxを除いた画像をテンプレートとして位置あわせを行なうか
    pad = 30

    ## 許容する最低マッチ度
    thresh = 0.7

    ## 総数
    total_num = len(theta_space) * len(pct_lambda_space)

    def __init__(self, draft_image, product_image):
        ## 画像
        self.draft_image = draft_image
        self.product_image = product_image

        ## 縦横の調整用
        self.rotate90 = False     # 画像の向きを変えるかどうか(Trueの場合は位置合わせ後、マッチ度が低ければ90度回転し再度位置合わせ)
        self.dim_H, self.dim_W = draft_image.shape[:2]
        self.pim_H, self.pim_W = product_image.shape[:2]
        self.rotation_repeat_num = 0     # 何回90度回転したか

        ## 結果を保存
        self.best_condition = []     # 最高点の時の回転角、縮小拡大率
        self.best_value = 0
        self.best_result = []
        self.d_img = []

    ## 角度と縮尺から回転行列の作成(シフトは無し)
    def get_rotation_matrix(self, theta, pct_lambda):
        rot_mat = np.array([
            np.cos(theta)*pct_lambda,
            np.sin(theta)*(-pct_lambda),
            0,
            np.sin(theta)*pct_lambda,
            np.cos(theta)*pct_lambda,
            0
        ]).reshape(2,3)

        return(rot_mat)

    ## 入力されたdraft_imageをBGRにした後、引数の行列でaffine変換する
    def affine_trans(self, rot_mat):
        size = self.draft_image.shape[:2][::-1]
        img_rot = cv2.warpAffine(self.draft_image.copy(), rot_mat, size, flags=cv2.INTER_CUBIC)
        #img_rot = cv2.resize(img_rot,size)
        #print("imgrot:{}".format(img_rot.shape))
        return(img_rot)

    ## 縦横の90度回転
    def adjust_direction(self, k):
        if k != 3:
            print(f"\r => rotate {90*(k+1)} degrees", end= "")
        if k == 3:
            print("\n")
        if len(self.draft_image.shape) ==2:
            transpose_img = self.draft_image.transpose(1,0)
        else:
            transpose_img = self.draft_image.transpose(1,0,2)
        img_rot = transpose_img[:,::-1].astype(np.uint8)

        self.rotation_repeat_num += 1

        return(img_rot)

    # 画像の周囲にpad pxの余白を加える
    def padding(self, image, pad):
        if image.ndim == 2:
            h,w = image.shape
            sc = np.zeros((h+2*pad,w+2*pad), dtype=image.dtype)
        else:
            h,w,c = image.shape
            sc = np.zeros((h+2*pad,w+2*pad,c), dtype=image.dtype)
        sc.fill(0)
        sc[pad:h+pad,pad:w+pad] = image
        return(sc)

    ## template matching
    def temp_match(self, draft_image, pad):
        ## テンプレートマッチングの準備(グレースケール)
        temp_gray = self.product_image.copy()
        pad_draft_image = self.padding(draft_image, pad)
        ref_gray = pad_draft_image

        ## 中心の切り取り
        template = temp_gray[pad:self.pim_H-pad, pad:self.pim_W-pad]
        ## テンプレートマッチング
        res = cv2.matchTemplate(ref_gray, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        x1, y1 = max_loc[0], max_loc[1]
        x2, y2 = x1 + self.pim_W, y1 + self.pim_H

        x = [x1, x2]
        y = [y1, y2]

        pad_pad_draft_image = self.padding(pad_draft_image,pad)
        return [pad_pad_draft_image[y[0]:y[1], x[0]:x[1]], max_val]

    ## 進捗状況の可視化
    def print_progress_bar(self, i, n, tl):
        s = ("="*int(np.round(20*(i+1)/n, 1))).ljust(20,"-")
        print("\r[{0:s}] : {1:e} : {2:d}/{3:d} ({4:d}%) : {5:e}".format(s, self.best_value, i+1, n, int(np.round((i+1)/n*100, 1)), tl), end="")
        if (i+1) == n:
            print("")

    ## 結果を追記・更新する
    def update(self, result, condition):
        if result[1] > Affined_temp_match.thresh and result[1] >= self.best_value:
            self.rotate90 = False
            self.best_condition = condition
            self.best_value = result[1]
            self.best_result = result[0]
        elif result[1] >= self.best_value:
            self.best_condition = condition
            self.best_value = result[1]
            self.best_result = result[0]
    ## 回転角度、縮尺の最適化
    def fit(self, rotation=True):
        for k in range(4):
            i = 0
            for tl in itertools.product(Affined_temp_match.theta_space, np.round(Affined_temp_match.pct_lambda_space, 2)):
                i += 1
                rot_mat = self.get_rotation_matrix(tl[0], tl[1])
                draft_image = self.affine_trans(rot_mat)

#                 try:
                self.update(self.temp_match(draft_image, Affined_temp_match.pad), tl)
#                 except Exception as e:
#                     print(e)
#                     with open("matching_error.txt", "a") as f:
#                         f.write(str(e))
#                     continue

            if (self.rotate90 == False) or (rotation == False):
                break
            else:
                self.draft_image = self.adjust_direction(k)

        if self.best_value < Affined_temp_match.thresh:
            #print(f"{self.best_value} < threshold score:{Affined_temp_match.thresh}\ Not match correctly")
            pass
        else:
            #print("\n match correctly")
            pass
    # def show_Affined_img(self):
    #      for tl in itertools.product(self.theta_space, np.round(Affined_temp_match.pct_lambda_space, 2)):
    #             rot_mat = self.get_rotation_matrix(tl[0], tl[1])
    #             draft_image = cv2.cvtColor(self.affine_trans(rot_mat), cv2.COLOR_BGR2RGB)
    #             plt.figure(figsize=(10,10))
    #             plt.imshow(draft_image)
    #             plt.show()

    ## 最善の時の画像セットを返す
    def best_one(self):
        return [self.draft_image, self.product_image, self.best_result]

def main():
    # Affined_temp_match(scan_image, RIP_image)でインスタンスの作成
    with open('/black/suzuki/workspace/toppan_20180802/OK_pickle/renew_images.pickle','rb') as f:
        scan_imgs, degi_imgs = pickle.load(f)
    im_set = Affined_temp_match(scan_imgs[0], degi_imgs[0])
    # fitで位置合わせ開始。methodはbinary, edge(未完), gray_scaleのいずれか　rotationは90度回転を行うかどうか
    # (回転角のグリッドや縮小拡大のグリッドは上のクラス変数で定義)
    im_set.fit(rotation=True)
    # scan_image, RIP_image, scan_imageの中でRIPと一致する領域、の3枚を返す
    result = im_set.best_one()

def temp_match(img_master, img_detect):
    """
    img_a.shape > img_b.shape
    img_bと似た部分をimg_aの中からマッチングで探すイメージ
    """
    im_set = Affined_temp_match(img_detect,img_master)
    im_set.rotate90 = False
    im_set.fit(rotation=False)
    img_detect, img_master_matched, img_detect_matched  = im_set.best_one()
    return img_master_matched, img_detect_matched
