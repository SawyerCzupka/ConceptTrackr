from langchain.llms import TextGen


def get_ooba_llm(model_url='http://localhost:5000', **kwargs):
    args = {
        'max_new_tokens': 1000
    }
    args.update(kwargs)

    return TextGen(model_url='http://localhost:5000', **args)
