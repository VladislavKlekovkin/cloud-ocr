def compare_results(ground_truth, predicted):
    
    if len(ground_truth) != len(predicted):
        print("Error. Different lengths")
        return
    
    correct = 0
    
    for gt, pred in zip(ground_truth, predicted):
        if gt.lower() == pred.lower():
            correct += 1
            
    result = 100 * correct/len(ground_truth)
    return round(result, 2)
