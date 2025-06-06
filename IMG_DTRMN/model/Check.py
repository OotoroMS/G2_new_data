import tensorflow as tf
from tensorflow import keras

# .kerasファイルのパス
model_path = "Sample2024_massive_quarter_50.keras"

# モデルの読み込み
model = keras.models.load_model(model_path)

# モデルの概要を表示
model.summary()

# 各レイヤーの情報を表示
for layer in model.layers:
    print(f"Layer name: {layer.name}")
    print(f"  Type: {type(layer)}")
    print(f"  Output shape: {layer.output_shape}")
    print(f"  Number of parameters: {layer.count_params()}")
    print()