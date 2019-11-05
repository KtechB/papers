# 論文まとめテストページ
# Imitation Learnings
## HGAIL
https://arxiv.org/pdf/1903.07854.pdf
Hind sight Transformationを利用して自らの行動から良い行動を抽出しself-imitation

##表現学習
https://speakerdeck.com/tmats/di-32hui-qiang-hua-xue-xi-akitekutiyamian-qiang-hui-zhuang-tai-biao-xian-xue-xi-toshi-jie-moderufalsezui-jin-falseyan-jiu-oyobishen-ceng-sheng-cheng-moderuraiburaripixyzfalseshao-jie-number-rlarch?slide=4
大枠

### Graph Laplacianによる距離学習
The Laplacian in RL: Learning Representations with Efficient Approximations
https://openreview.net/forum?id=HJlNpoA5YQ
（GraphにおけるLaplacianの基本https://qiita.com/ryunryunryun/items/297b54a59172b43b3f20)
###  SQIL
https://arxiv.org/abs/1905.11108z

### Directed-InfoGAIL (ICLR2019)
info-GAILの潜在変数について遷移条件を考慮　option GANにちかい
https://arxiv.org/abs/1810.01266

Multi-Modal Imitation Learning from Unstructured Demonstrations using Generative Adversarial Nets
http://papers.nips.cc/paper/6723-multi-modal-imitation-learning-from-unstructured-demonstrations-using-generative-adversarial-nets
infoGAILとほぼ同じ
適用タスクがMujocoを中心としており，Reacherなどのtargetをいじった結果が記載されている．

### Imitation Learning from Imperfect Demonstration
https://arxiv.org/abs/1901.09387
confidenceというスコアを付加したsuboptimalデモンストレーションを用いて，学習


### Residual RL(using Residual algolithm)
https://arxiv.org/abs/1905.01072

### Residual poliy learning
https://arxiv.org/abs/1812.06298
与えられたタスクに対して不完全な制御方策が得られている場合を想定し，与えられた初期方策を改善しながら，少ない試行回数で適切な方策を獲得することを実現する

### Auto RL(tune reward for Mujoco)
https://arxiv.org/pdf/1905.07628

### Dyna-AIL : Adversarial Imitation Learning by Planning
https://arxiv.org/abs/1903.03234
GAIL + Dyna(?)

# model base
https://www.slideshare.net/DeepLearningJP2016/dlsimpleimproved-dynamics-modelplanet-vaerl

## Robots that Learn to Adapt
エージェントのモデル変化への適応
https://bair.berkeley.edu/blog/2019/05/06/robot-adapt/

# Hierarchical
https://www.slideshare.net/yukono1/nips2017pfn-hierarchical-reinforcement-learning

# Application
LEARNING TO NAVIGATE THE WEB
https://openreview.net/forum?id=BJemQ209FQ
web操作エージェントの学習
デモがあるときはカリキュラムラーニング
ない時もmeta学習したカリキュラムトレーナーで学習？？
large state action space
sparse reward
### R2P2: A ReparameteRized Pushforward Policy for Diverse, Precise Generative Path Forecasting
https://www.cs.cmu.edu/~nrhineha/R2P2.html
自動車の経路予測

### Imitation Learning for Human Pose Prediction
https://arxiv.org/abs/1909.03449
GAILによる姿勢予測（max 1[sec])
### Socially Compliant Navigation through Raw Depth Inputs with Generative Adversarial Imitation Learning
歩行者をよけるロボットをraw input GAILで実現
↓データなど公開済み
https://github.com/onlytailei/gym_ped_sim

###Learning temporal strategic relationships using generative adversarial imitation learning
潜在状態を含めた自動運転

### Preferences Implicit in the State of the World
https://arxiv.org/abs/1902.04198
環境から人の嗜好を推定？？
