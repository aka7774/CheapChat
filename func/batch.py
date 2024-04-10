import json
import tqdm
import datetime

import func.prompt
import func.models

def run(b_options, b_prompts, b_models, b_temps, b_inputs):
    opt = json.loads(b_options)
    ps = b_prompts.splitlines()
    ms = b_models.splitlines()
    temps = b_temps.splitlines()
    inputs = b_inputs.splitlines()

    prompts = func.prompt.load_prompts()

    path = f"log/batch_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    for m in tqdm.tqdm(ms):
        try:
            mopt = func.models.models[m]
            mopt.update(opt)
        except:
            mopt = opt.copy()

        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"model_name: {m}\n")
            f.write(f"options: {json.dumps(mopt)}\n")

        for p in tqdm.tqdm(ps, leave=False):
            instruction = prompts[p]
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"{instruction}\n")

            for t in tqdm.tqdm(temps, leave=False):

                with open(path, 'a', encoding='utf-8') as f:
                    f.write(f"temperature: {t}\n")
                    f.write("====\n")

                for input in tqdm.tqdm(inputs, leave=False):
                    mopt['model_name'] = m
                    mopt['temperature'] = float(t)

                    res = None
                    proceed = None
                    time = None
                    try:
                        res, proceed, time = func.prompt.infer_prompt(instruction, input, mopt)
                    except Exception as e:
                        with open(path, 'a', encoding='utf-8') as f:
                            f.write(f"{e}\n")

                    with open(path, 'a', encoding='utf-8') as f:
                        f.write(f"input: {input}\n")
                        f.write("----\n")
                        # if proceed:
                            # f.write(f"{proceed}\n")
                            # f.write("----\n")
                        if res:
                            f.write(f"{res}\n")
                        if time:
                            f.write(f"{time}\n")
                        f.write("====\n")

    print(f"{path} saved.")
    return f"{path} saved."
