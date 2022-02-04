import picar_4wd as fc


def avoid():
    while 1:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue
        left,middle,right = scan_list[:5], scan_list[2:5], scan_list[3:]
        if middle != [2,2,2]:
            if left == [2,2,2,2]:
                fc.turn_left(30)
            elif right == [2,2,2,2]:
                fc.turn_right(30)
        else:
            fc.forward(50)

        
        
