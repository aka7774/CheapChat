import json
import tqdm
import datetime

import func.prompt
import func.models

def run(b_options, b_prompts, b_models, b_temps, b_input):
    opt = json.loads(b_options)
    ps = b_prompts.splitlines()
    ms = b_models.splitlines()
    temps = b_temps.split()

    prompts = func.prompt.load_prompts()

    path = f"log/batch_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    for m in tqdm.tqdm(ms):
        try:
            mopt = func.models.models[m]
            mopt.update(opt)
        except:
            mopt = opt.copy()

        for p in tqdm.tqdm(ps, leave=False):
            instruction = prompts[p]
            for t in tqdm.tqdm(temps, leave=False):
                mopt['model_name'] = m
                mopt['temperature'] = float(t)

                res = None
                proceed = None
                try:
                    res, proceed = func.prompt.infer_prompt(instruction, b_input, mopt)
                except Exception as e:
                    print(e)
                    with open(path, 'a', encoding='utf-8') as f:
                        f.write("ERROR\n")

                with open(path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(mopt)+"\n")
                    if res:
                        f.write(res+"\n")
                    if proceed:
                        f.write(proceed+"\n")

    print(f"{path} saved.")
    return f"{path} saved."
