import boto3
from tqdm import tqdm
from datasets import datasets
from utils import compare_results

client=boto3.client('rekognition')


def reformat_aws_response(response):
    
    result = ""
    
    for box in response['TextDetections']:
        if box['Type'] == "WORD":
            result += box['DetectedText']
    
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

            response = client.detect_text(Image={'Bytes': content})
            result = reformat_aws_response(response)

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
