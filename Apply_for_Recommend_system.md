# Recommend system
##従来手法
###CF
ユーザーやアイテムごとに似たもの同士は似た嗜好を持つという考え
同じような行動をする人は同じものを好む説を利用
問題点 
- データが足りない（スパースデータ）
- ユーザかアイテムどちらかしか考えれていない．
- Static

##強化学習を用いるメリット
将来的な報酬を含めて学習が可能．


# papers for Recommendation

## Reinforcement Learning based Recommender Systemusing Biclustering Technique
グリッドワールドに落とし込む？
https://arxiv.org/abs/1801.05532

## Stabilizing Reinforcement Learning in Dynamic Environmentwith Application to Online Recommendation
https://dl.acm.org/citation.cfm?id=3220122
KDD2018
動的環境へのロバスト性を工夫
- Stratified sampling replay
- regret reward :もともとバンディット問題での考え．regret$\rho$はT回の試行での最適方策と実際の得られた報酬の差
