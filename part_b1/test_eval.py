from eval import evaluate_per_type
from pprint import pprint

reference = {("Maria Gomez", "PER"),
             ("Northwind Logistics", "ORG"),
             ("Denver", "LOC")}
prediction = {("Maria Gomez", "PER"),
             ("Northwind Logistics", "ORG"),
             ("Denver", "ORG")} 

def main():
    eval_results = evaluate_per_type(reference, prediction)
    pprint(eval_results)

if __name__=="__main__":
    main()