def compare(img1, img2):
    pic1 = img1.load()
    pic2 = img2.load()
    w,h = size1 = img1.size
    size2 = img2.size
    if size1 != size2:
        return False
    for x in range(w):
        for y in range(h):
            if pic1[x,y]!=pic2[x,y]:
                return False
    return True

