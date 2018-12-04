# import os
# import sys
# sys.path.insert(0,  os.getcwd())
# print(os.getcwd())
from Product.createsubscribtion import subscribtion

if __name__ == '__main__':
    import sys

    subType = {
        "bronze": [20000, 1],  # 169
        "silver": [100000, 1],  # 289
        "platinium": [500000, 1],  # 699
        "gold": [500000, 6],  # 1499
        "diamond": [9999999999, 12],  # 3699
        "special": [100000, 3],  # 3699
        "admin": [100000, 12]  # 3699
    }
    print("subscribtion type:",subType)
    if(len(sys.argv)==3):
        subscribtion(sys.argv[0],sys.argv[1],sys.argv[2])
    else:
        print("(username,password,subscribtion type)")

