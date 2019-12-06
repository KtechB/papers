Transpoter KeyPoint learnin

# intro
問題：表現はもっと一般的であるべき．
セグメンテーションの分野ではkeypointを

apply to
-1 key pointをRGB画像の代わりに使用してRL　データ効率up
-2 直交座標をコントロールすることによるスキル(optionを学習する)

# method
## Keypoint抽出方法
Goal:keynetでK個のkeypointを抽出 するKeynetを学習
学習:sourceとtargetの2画像についてそれぞれfeatureとkeypointを抽出
2画像からkeypoint部分を取り除いた特徴量　＋targetのkeypoint部分の特徴量　
を用いて，target画像をreconstructするように学習

　
## RLへの適用
keypointそのものを特徴量とするor 重みづけた特徴量を使うｓ

actionの表現学習
keypointを各方向に移動させる方策を学習するｓ
一番動きやすいpointをplayerだとして判断も可能