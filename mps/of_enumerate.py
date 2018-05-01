def of_enumerate(the_list):
    zfills = len(str(len(the_list)))
    length_list = len(the_list)
    for i, item in enumerate(the_list):
        i = str(i + 1).zfill(zfills)
        yield '{i} / {length_list}'.format(i=i, length_list=length_list), item

    raise StopIteration
