import json
from monomax import get_list_of_monomax
from ziko import get_list_of_ziko
from kfc import get_list_of_kfc


list_of_kfc = get_list_of_kfc()
list_of_ziko = get_list_of_ziko()
list_of_monomax = get_list_of_monomax()


def main():
    try:
        with open("data_file.json", "w") as write_file:
            json.dump(list_of_kfc, write_file)
            json.dump(list_of_ziko, write_file)
            json.dump(list_of_monomax, write_file)
    except Exception as e:
        print(f'Json file error is {e}')


if __name__ == "__main__":
    main()
    print('Json file generated successfully!')
