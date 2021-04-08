"""
This module creat data generators for the following datasets:
IIIT5K, IC13, SVHN
"""
import scipy.io
import mat73

len_IIIT5K = 500 # max 3000
len_IC13 = 500   # max 848
len_SVHN = 500   # max 13068

path_IIIT5K = 'data/IIIT5K/'
file_IIIT5K = path_IIIT5K + 'testdata.mat'

path_IC13 = 'data/Challenge2_Training_Task3_Images_GT/'
file_IC13 = path_IC13 + 'gt.txt'

path_SVHN = 'data/test/'
file_SVHN = path_SVHN + 'digitStruct.mat'


def get_label(content): # for SVHN
    
    label = ''
    
    if type(content) == list:
        
        for v in content:
            v = int(v.item())
            if v == 10: v = 0 
            label += str(v)
    else:
        v = int(content.item())
        if v == 10: v = 0   
        label += str(v)
        
    return label


def generator_IIIT5K(desc, len_):
    
    for i, row in enumerate(desc['testdata'][0]):
        if i >= len_:
            return
        
        yield path_IIIT5K + row[0][0], row[1][0]
        
        
def generator_IC13(desc, len_):
    
    for i, row in enumerate(desc):
        if i >= len_:
            return
        
        split = row.split(', ')
        
        yield path_IC13 + split[0], split[1][1:-2]
        
        
def generator_SVHN(desc, len_):  
    
    for i, img_name in enumerate(desc['digitStruct']['name']):
        if i >= len_:
            return
        
        data = desc['digitStruct']['bbox'][i]['label']
        label = get_label(data)
        
        yield path_SVHN + img_name, label

        
def postprocessing_IIIT5K(predicted):
    
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    
    for i, content in enumerate(predicted):
        
        result = ""
        
        for char in content:
            if char not in punc:
                result += char
        
        predicted[i] = result
        
    return predicted


def postprocessing_IC13(predicted):
    return predicted


def postprocessing_SVHN(predicted):
    return predicted


gt_IIIT5K = scipy.io.loadmat(file_IIIT5K)
gt_IC13 = open(file_IC13, 'r')
gt_SVHN = mat73.loadmat(file_SVHN, 'r')

gen_IIIT5K = generator_IIIT5K(gt_IIIT5K, len_IIIT5K)
gen_IC13 = generator_IC13(gt_IC13, len_IC13)
gen_SVHN = generator_SVHN(gt_SVHN, len_SVHN)

datasets = {
    "IIIT5K":{"gen":gen_IIIT5K, 
              "len":len_IIIT5K, 
              "postprocessing": postprocessing_IIIT5K},
    "IC13":  {"gen":gen_IC13, 
              "len":len_IC13, 
              "postprocessing": postprocessing_IC13},
    "SVHN":  {"gen":gen_SVHN, 
              "len":len_SVHN, 
              "postprocessing": postprocessing_SVHN}  
}
