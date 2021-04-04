# from sqllex import *
# columns = {
#         "username": [TEXT, NOT_NULL],
#         "group_id": INTEGER,
#
#         FOREIGN_KEY: {
#             "group_id": ["groups", "group_id"]
#         },
#     }
#
# temp = "TEMP"
# name = "groups"
# if_not_exist = True
#
# result: str = ''
#
# # column-def
# for (col, params) in columns.items():
#     if isinstance(params, (str, int, float)):
#         params = [f"{params}"]
#
#     if isinstance(params, list):
#         result += f"{col} {' '.join(param for param in params)},\n"
#
#     elif isinstance(params, dict) and col == FOREIGN_KEY:
#         res = ''
#         for (key, refs) in params.items():
#             res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
#         result += res[:-1]
#
#     else:
#         raise TypeError

if __name__ == '__main__':
    pass

