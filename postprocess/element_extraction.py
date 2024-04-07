import argparse
from datasets import load_dataset
from tqdm import tqdm
import json


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--set_type", type=str, default="validation")
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo-1106")
    parser.add_argument("--mode", type=str, default="two-stage")
    parser.add_argument("--strategy", type=str, default="direct")
    parser.add_argument("--output_dir", type=str, default="./")
    parser.add_argument("--tmp_dir", type=str, default="./")

    args = parser.parse_args()

    if args.mode == 'two-stage':
        suffix = ''
    elif args.mode == 'sole-planning':
        suffix = f'_{args.strategy}'


    results = open(f'{args.tmp_dir}/{args.set_type}_{args.model_name}{suffix}_{args.mode}.txt','r').read().strip().split('\n')
    
    if args.set_type == 'validation':
        query_data_list  = load_dataset('osunlp/TravelPlanner','validation')['validation']
    elif args.set_type == 'test':
        query_data_list  = load_dataset('osunlp/TravelPlanner','test')['test']
    print(args)
    idx_number_list = [i for i in range(1,len(query_data_list)+1)]
    for idx in tqdm(idx_number_list[:]):
        generated_plan = json.load(open(f'{args.output_dir}/{args.model_name}_{args.set_type}/{args.mode}/generated_plan_{idx}.json'))
        print("path:",f'{args.output_dir}/{args.model_name}_{args.set_type}/{args.mode}/generated_plan_{idx}.json')
        #print(generated_plan)
        if generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_results'] not in ["","Max Token Length Exceeded."] :
            #print ("generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_results']:",generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_results'])
            try:
                result = results[idx-1].split('```json')[1].split('```')[0]
            except:
                print(f"{idx}:\n{results[idx-1]}\nThis plan cannot be parsed. The plan has to follow the format ```json [The generated json format plan]```(The common gpt-4-preview-1106 json format). Please modify it manualy when this occurs.")
                print(f"generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_results']:{generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_results']}")
                continue
                break
            try:
                if args.mode == 'two-stage':
                    generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_parsed_results'] = eval(result)
                else:
                    generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_parsed_results'] = eval(result)
            except:
                print(f"{idx}:\n{result}\n This is an illegal json format. Please modify it manualy when this occurs.")
                break
        else:
            if args.mode == 'two-stage':
                generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_parsed_results'] = None
            else:
                generated_plan[-1][f'{args.model_name}{suffix}_{args.mode}_parsed_results'] = None
  
        with open(f'{args.output_dir}/{args.set_type}/generated_plan_{idx}.json','w') as f:
            json.dump(generated_plan,f)