a = (
    ((1, (2, (3,))),),
    (1, 2)
)


def lister(ret_):
    if isinstance(ret_, tuple):
        ret_ = list(ret_)

    if isinstance(ret_, list):
        if len(ret_) == 1:
            return lister(ret_[0])

        for r in range(len(ret_)):
            ret_[r] = lister(ret_[r])

    return ret_

a = lister(a)

print(a)



