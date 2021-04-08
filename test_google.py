import os
from tqdm import tqdm
from google.cloud import vision
from datasets import datasets
from utils import compare_results

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = 'YOUR CREDENTIALS'

client = vision.ImageAnnotatorClient()

def reformat_google_response(response):
    
    result = ''
    
    texts = response.text_annotations
    for idx, text in enumerate(texts):
        if idx:
            result += text.description
    
    return result
    
def get_accuracy(datasets):
    accuracy = {}
    for dname in datasets:

        ground_truth = []
        predicted = []
        
        data = datasets[dname]
        for image_path, label in tqdm(data["gen"], total=data["len"]):
            
            with open(image_path, 'br') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.text_detection(image=image)

            result = reformat_google_response(response)

            ground_truth.append(label)
            predicted.append(result)
        
        postprocessing = datasets[dname]["postprocessing"]
        predicted = postprocessing(predicted)
        
        accuracy[dname] = compare_results(ground_truth, predicted)
        
    return accuracy
    
if __name__ == "__main__":
    accuracy = get_accuracy(datasets)
    for key in accuracy:
        print(key, ": ", accuracy[key])    
