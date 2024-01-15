import transformers as tf
from fastapi import FastAPI
from pydantic import BaseModel

# create API instance
app = FastAPI()

# Function to load and cache models
def load_model(username, prefix, model_name):
    p = tf.pipeline('text-classification', f'{username}/{prefix}-{model_name}', top_k=None)
    return p

def get_results(model, comments):
    results = model(comments)
    comment_labels = []
    # a sorted array of labels are returned for each model with the first label being the one that the model gives the higest score
    # so for each comment result we pick the zero index label and get its label ID so label_5 for example gives us 5. 
    for result in results:
        comment_labels.append(int(result[0]['label'].split('_')[1]))
    return comment_labels

def run_models(model_names, models, comments):
    model_results = {}
    comment_label_list=[]
    for mn in model_names:
        model_results[mn] = get_results(models[mn], comments)
    
    for idx, x in enumerate(comments):
        comment_labels_entry = {}
        for mn in model_names:
            comment_labels_entry[mn] = model_results[mn][idx]
            
        #Modify results to sum the QuAL score and to ignore Q3 if Q2 has no suggestion
        if comment_labels_entry['q2i'] == 1:
            comment_labels_entry['q3i'] = 1 # can't have a linked suggestion if no suggestion is given

        # The overall qual score is a summation of the three model scores, q2i and q3i are negated such that comments with suggestions are given a higher score
        comment_labels_entry['qual'] = comment_labels_entry['q1'] + (not comment_labels_entry['q2i']) + (not comment_labels_entry['q3i'])
        comment_label_list.append(comment_labels_entry)
    
    # return a list of comments each with their individual model labels
    return comment_label_list;
              

# Load models
# Specify which models to load 
USERNAME = 'maxspad'
PREFIX = 'nlp-qual'
models_to_load = ['q1', 'q2i', 'q3i']
models = {}

for i, mn in enumerate(models_to_load):
    models[mn] = load_model(USERNAME, PREFIX, mn)
print('Model Loading Complete')

class InputModel(BaseModel):
    comments: list[str]
    
@app.post("/generate-qualscore")
def predict_qualscore(payload: InputModel):
    comments = payload.comments
    # Run the models on the comment list
    results = run_models(models_to_load, models, comments)
    return [results]


