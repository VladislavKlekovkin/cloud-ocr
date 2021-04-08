import time
from tqdm import tqdm
from datasets import datasets
from utils import compare_results
from PIL import Image
from io import BytesIO

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "YOUR KEY"
endpoint = "YOUR ENDPOINT"

computervision_client = ComputerVisionClient(endpoint, 
                                             CognitiveServicesCredentials(subscription_key))
                                             
def reformat_azure_response(response):
    
    result = ""
    
    for line in response['analyze_result']['read_results'][0]['lines']:
        result += line['text']
        
    return result


def resize(img):
    
    _format = img.format
    
    size = tuple(max(val, 50) for val in img.size)
    img = img.resize(size)
    
    img.format = _format
    
    return img


def get_image_file_object(image_path):
    
    byte_arr = BytesIO()
    img = Image.open(image_path)
    img = resize(img)
    img.save(byte_arr, img.format)
    byte_arr.seek(0)
    
    return byte_arr
    
    
def get_accuracy(datasets):
    accuracy = {}
    for dname in datasets:

        ground_truth = []
        predicted = []
        
        data = datasets[dname]
        for image_path, label in tqdm(data["gen"], total=data["len"]):
            
            image = get_image_file_object(image_path)
            job = computervision_client.read_in_stream(image=image, raw=True)

            operation_id = job.headers['Operation-Location'].split('/')[-1]
            image_analysis = computervision_client.get_read_result(operation_id)
            
            while image_analysis.status in ['notStarted', 'running']:
                time.sleep(1)
                image_analysis = computervision_client.get_read_result(
                    operation_id=operation_id)

            response = image_analysis.as_dict()

            result = reformat_azure_response(response)

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
