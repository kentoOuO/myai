import asyncio
import os
os.environ["HTTP_PROXY"] = "127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "127.0.0.1:7897"
from googletrans import Translator
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
import json

# 使用新的方式加载预训练的 ResNet-18 模型
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 将模型设置为评估模式
model.eval()

# 这里使用一个从网络上下载的图片，实际使用时你可以加载本地图片
img = Image.open("641.webp")

# 定义图像预处理操作
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),  # 转为 Tensor 类型
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # 归一化
])

# 对图片进行预处理
img_tensor = preprocess(img)
# 增加一个维度，表示 batch size
img_tensor = img_tensor.unsqueeze(0)

# 禁用梯度计算
with torch.no_grad():
    outputs = model(img_tensor)

# 输出结果是一个包含 1000 个类的概率分布（如果是分类任务）
_, predicted_class = torch.max(outputs, 1)

# 打印预测的类别索引
print(predicted_class)

# 下载 ImageNet 类别标签
LABELS_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json'
response = requests.get(LABELS_URL)
class_idx = json.loads(response.text)

# 获取预测的标签名称
predicted_label = class_idx[str(predicted_class.item())][1]
print(f"Predicted label: {predicted_label}")


async def translate_text(text, target='en'):
    translator = Translator()
    result = await translator.translate(text, dest=target)
    return result.text


async def main():
    text = await translate_text(predicted_label, target='zh-cn')
    print(text)
    pass

# Run the async function
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())