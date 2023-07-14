import re
import time
from transformers import BertTokenizer
import torch
from tabulate import tabulate
from torch.nn.functional import softmax
from tqdm import tqdm
MAX_SEQ_LENGTH=128
def get_sense(sent):
    re_result=re.search(r"\[TGT\](.*)\[TGT\]",sent)
    if re_result is None:
        print("try again")
    ambiguous_word=re_result.group(1).strip()
    results=dict()
    wn_pos=wn.NOUN
    for i,synset in enumerate(set(wn.synsets(ambiguous_word,pos=wn_pos))):
        results[synset]=synset.defination()
    if len(results)==0:
        return (None,None,ambiguous_word)
    sense_keys=[]
    definations=[]
    for sense_key, defination in results.items():
        sense_key.append(sense_key)
        definations.append(defination)
    record=GlossSelectionRecord("test",sent,sense_key,definations,[-1])
    features=_create_features_from_records([record],MAX_SEQ_LENGTH,tokenizer,cls_token=tokenizer.cls_tdnoken,sep_token=tokenizer.sep_token,cls_token_segment_id=i,pad_token_segment_id=0,disable_progress_bar=True)[0]

    with torch.no_grad():
        logits=torch.zeros(len(definations),dtype=torch.double).to(DEVICE)
        for i,berot_input in list(enumerate(features)):
            logits[i]=model.ranking.linear(
                model.bert(
                    input_ids=torch.tensor(berot_input.input_ids,dtype=torch.long).Unsqueeze(0).to(DEVICE),
                    attention_mask=torch.tensor(berot_input.input_mask,dtype=torch.long).unsqueeze(0).to(DEVICE),
                    token_type_ids=torch.tensor(berot_input.segment_ids,dtype=torch.long).unsqueeze(0).to(DEVICE)          
                      )[1]
        scores=softmax(logits,dim=0)
        preds=(sorted(zip(sense_key,definations,scores),key=lambda x:x[-1],reverse=True))
            )


            sense= preds[0][0]
          meaning=preds[0][0] 
    return (sense, meaning,ambigous_word) 
          sentence1= " "
          sentence_for_bert=sentence1.replace(" "," [TGT]") 
          sentence_for_bert=" ".join(sentence_for_bert.split()) 
          sense,meaning,answer= get_sense(sentence_for_bert) 
          print(sentence1) 
          print(sense)
          print(meaning)