from my_functions import execute_this


def write_file(file_name: str, text: str):
    with open(file_name, 'a') as f:
        f.write(text)


def write_ordered_dict(*, file_name: str, ordered_dict: dict):
    new_dict = {}
    for key in ordered_dict.keys():
        new_dict[int(key.split('.')[0])] = ordered_dict[key]

    for idx, key in enumerate(sorted(new_dict.keys())):
        print(key)
        write_str = " ".join((img_name for img_name, _ in sorted(new_dict[key], key=lambda x: x[1], reverse=True)))
        write_file(file_name, f"Q{idx + 1}:" + write_str + "\n")


def show_top_20(*, ordered_dict: dict):
    new_dict = {}
    for key in ordered_dict.keys():
        new_dict[int(key.split('.')[0])] = ordered_dict[key]

    for idx, key in enumerate(sorted(new_dict.keys())):
        print(f"Q{idx + 1}:", end='')
        for index, result in enumerate(sorted(new_dict[key], key=lambda x: x[1], reverse=True)):
            if index < 10:
                print(f"{result[0]}", end=' ')
        print()
