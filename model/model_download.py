from tensorflow.keras.applications import resnet50

model = resnet50.ResNet50(include_top=True, weights="imagenet")