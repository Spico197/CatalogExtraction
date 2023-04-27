import json
import readline


def format_prf1_dict(data):
    print(f"{100 * data['p']:.3f}/{100 * data['r']:.3f}/{100 * data['f1']:.3f}")


if __name__ == "__main__":
    input_string = ""
    while True:
        input_string = input(">>>")
        if input_string == "q!":
            break
        format_prf1_dict(eval(input_string))
