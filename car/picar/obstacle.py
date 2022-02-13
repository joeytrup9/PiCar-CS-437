import picar_4wd as fc


def avoid():
    backward = False
    while 1:
        scan_list = fc.scan_step(35)
        
        print("scanned")
        print(scan_list)
        if not scan_list:
            continue
        
        if len(scan_list) == 5:
            continue
        
        left,middle,right = scan_list[:4], scan_list[3:7], scan_list[6:]
        print("left = " + str(left))
        print("right = " + str(right))
        print("middle = " + str(middle))
        
        if not backward:
            print("not backwards")
            if middle != [2,2,2,2]:
                print("middle has obstacle")
                if left == [2,2,2,2]:
                    #print(left)
                    print("forwards - left is free")
                    fc.turn_left(30)
                elif right == [2,2,2,2]:
                    #print(right)
                    print("forwards - right is free")
                    fc.turn_right(30)
                else:
                    print("go backwards from forwards")
                    fc.backward(30)
                    backward = True
            else:
                print("continue forwards")
                fc.forward(50)
                
        else:
            if left == [2,2,2,2]:
                #print(left)
                print("backward - left is free")
                fc.turn_left(30)
                backward = False
            elif right == [2,2,2,2]:
                #print(right)
                print("backward - right is free")
                fc.turn_right(30)
                backward = False
            else:
                print("continue backwards")
                fc.backward(15)
            

avoid()


