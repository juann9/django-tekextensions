

def normalize_model_name(model_name):
    if model_name.lower() == model_name:
        normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name

    return normal_model_name
