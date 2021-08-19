# 理論
y[n] = 1/n Σ_{k=0}^{n-1} x[n-k]

両辺X変換 -> Y(z) = 1/n Σ_{k=0}^{n-1} z^{-k}X(z)

伝達関数 H(z) = 1/n Σ_{k=0}^{n-1}z^{-k} -①

伝達関数の一般形 H(Z) = Σ_{k=0}^{n-1}b_k * x^{-k} / Σ_{k=0}^{n-1}a_k * x^{-k} -②

①, ②を比較すると、a_k = 0, b_k = 1/n

# 参考
* 読み込んだバイナリ形式のデータを変換する部分

    [[備忘録]pythonのwaveモジュール](https://qiita.com/bayachin/items/68f7659d31fa6c836317)

* フィルタの部分

    [６．コンサートホールの反響を再現しよう](https://keep-learning.hatenablog.jp/entry/2019/07/28/000000)
