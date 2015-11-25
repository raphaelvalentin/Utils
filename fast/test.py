def nearest3(cflist, n, value, index):
    # initialize
    index[0] = 0
    ci0 = cflist[0] - value
    if ci0 < 0:
        ci0 = -ci0
    index[1] = 1
    ci1 = cflist[1] - value
    if ci1 < 0:
        ci1 = -ci1
    index[2] = 2
    ci2 = cflist[2] - value
    if ci2 < 0:
        ci2 = -ci2
    # sort
    if ci2 < ci1:
        t = ci1
        ci1 = ci2
        ci2 = t
    if ci1 < ci0:
        t = ci0
        ci0 = ci1
        ci1 = t
    if ci2 < ci1:
        t = ci1
        ci1 = ci2
        ci2 = t
    for i in range(3, n, 1):
        ci = cflist[i] - value
        if ci < 0:
            ci = -ci
        if ci < ci0:
            index[2] = index[1]
            index[1] = index[0]
            index[0] = i
            ci2 = ci1
            ci1 = ci0
            ci0 = ci
        elif ci < ci1:
            index[2] = index[1]
            index[1] = i
            ci2 = ci1
            ci1 = ci
        elif ci < ci2:
            index[2] = i
            ci2 = ci



l=[0,1,2,3,4,5,6]
index = [0, 0, 0]
nearest3(l, len(l), 4.2, index)
print index

