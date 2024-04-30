from flask import Flask, request, jsonify
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoTokenizer, ViTFeatureExtractor, VisionEncoderDecoderModel

app = Flask(__name__)

# Load pretrained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.unk_token
model = VisionEncoderDecoderModel.from_pretrained("C:/Users/KIIT/Desktop/Major Project/working/image_captioning_model")
model = model.to(device)
model.eval()

# Define image preprocessing transformation
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
])

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    img = Image.open(file).convert("RGB")
    img_tensor = preprocess(img).unsqueeze(0).to(device)

    # Generate caption
    generated_ids = model.generate(pixel_values=img_tensor)
    generated_caption = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return jsonify({'caption': '. '.join(generated_caption.split('.')[:2])})

if __name__ == '__main__':
    app.run(debug=True)