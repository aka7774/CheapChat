import func.provider.trllm
import func.provider.ollama
import func.provider.openai
import func.provider.anthropic
import func.provider.googleai

def infer(instruction = '', input = '', messages = {}, opt = {}):
    provider = opt['provider']
    del opt['provider']

    speech = None
    res = None

    match provider:
        case 'trllm':
            res = func.provider.trllm.infer(
                instruction, input, messages, opt,
            )
            speech = func.provider.trllm.content(res)
        case 'ollama':
            res = func.provider.ollama.infer(
                instruction, input, messages, opt,
            )
            speech = func.provider.ollama.content(res)
        case 'openai':
            res = func.provider.openai.infer(
                instruction, input, messages, opt,
            )
            speech = func.provider.openai.content(res)
        case 'anthropic':
            res = func.provider.anthropic.infer(
                instruction, input, messages, opt,
            )
            speech = func.provider.anthropic.content(res)
        case 'googleai':
            res = func.provider.googleai.infer(
                instruction, input, messages, opt,
            )
            speech = func.provider.googleai.content(res)
        case _:
            raise ValueError('invalid provider: ' + provider)

    return speech, res

tsv = []

def trim_output(output):
    global tsv
    for row in tsv:
        if len(row) > 2 and row[2] == 'resub':
            rep = re.compile(row[0], re.MULTILINE | re.DOTALL)
            output = re.sub(rep, row[1], output)
        elif row[0] in output:
            if len(row) == 1:
                row[1] = ''
            output = output.replace(row[0], row[1])

    return output
