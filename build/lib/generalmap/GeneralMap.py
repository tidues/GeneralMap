import types

class GMap:
    def __init__(self, recDepth=None, intoStr=False):
        self.resetDepth(recDepth)
        self.intoStr = intoStr
        self.basicTypes = {int: None, float: None, bool: None}
        self.structTypes = {
                list: self.__listMapRule,
                tuple: self.__tupleMapRule,
                dict: self.__dictMapRule,
                slice: self.__sliceMapRule,
                range: self.__rangeMapRule
                }
        if intoStr is True:
            self.structTypes[str] = self.__strMapRule
        else:
            self.basicTypes[str] = None
    
    # register new basic types
    def regBasicType(self, cls):
        if cls in self.structTypes.keys():
            del self.structTypes[cls]

        self.basicTypes[cls] = None

    # register new structure types
    def regStructType(self, cls, clsRule):
        if cls in self.basicTypes.keys():
            del self.basicTypes[cls]

        self.structTypes[cls] = clsRule
    
    # change depth
    def resetDepth(self, depth = None):
        errStr = str(depth) + ' is not a valid input. Depth is either None or positive integer.'
        if depth is not None:
            if type(depth) is int:
                if depth >= 1:
                    self.recDepth = depth
                else:
                    print(errStr)
            else:
                print(errStr)
        else:
            self.recDepth = None

    # update depth
    def __updateRunDepth(self, depth):
        if self.runDepth is None:
            self.runDepth = depth

    # user function, wrapper for the main function
    def gMap(self, f, struct):
        self.runDepth = self.recDepth
        if self.intoStr is True:
            self.passStr = False
        return self.__gMapRec(f, struct, 0)

    # main function, run gmap on structure
    def __gMapRec(self, f, struct, finishedDepth):
        if struct is None:
            # dealing with none value
            try:
                res = f(struct)
            except:
                res = None
            self.__updateRunDepth(finishedDepth)
            return res
        else:
            if self.runDepth is not None:
                if finishedDepth == self.runDepth:
                    return f(struct)
            else:
                # auto stop if no recursive depth defined
                if type(struct) in self.basicTypes:
                    self.__updateRunDepth(finishedDepth)
                    return f(struct)
                
        # get constructor and map rules for common structures
        mytype = type(struct)
        if mytype in self.structTypes.keys():
            ruleFun = self.structTypes[mytype]
        else:
            errStr = str(struct) + ' is not a supported type, please register this type along with a map rule function.'
            raise TypeError(errStr)

        isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc  = ruleFun(struct)

        # if bottom case, then apply function and return
        if isBottom is True:
            self.__updateRunDepth(finishedDepth)
            return f(struct)

        # map to parameters recusively
        for idx in paramMapIdx:
            paramList[idx] = liftFunc(paramList[idx], self.__gMapRec(f, projFunc(paramList[idx]), finishedDepth+1))

        if ifExpand:
            return const(*paramList)
        else:
            return const(paramList)

    # constructor and map rule for common structures
    def __listMapRule(self, struct):
        isBottom = False
        const = list
        paramList = struct
        paramMapIdx = range(len(paramList))
        ifExpand = False
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

    def __tupleMapRule(self, struct):
        isBottom = False
        const = tuple
        paramList = list(struct)
        paramMapIdx = range(len(paramList))
        ifExpand = False
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

    def __dictMapRule(self, struct):
        isBottom = False
        const = lambda lst: {key: value for (key, value) in lst}
        paramList = list(struct.items())
        paramMapIdx = range(len(paramList))
        ifExpand = False
        projFunc = lambda x: x[1]
        liftFunc = lambda x, res: (x[0], res)
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

    def __sliceMapRule(self, struct):
        isBottom = False
        const = slice
        if struct.start is None:
            start = 0
        else:
            start = struct.start
        if struct.step is None:
            step = 1
        else:
            step = struct.step
        paramList = [start, struct.stop, step]
        paramMapIdx = [0, 1]
        ifExpand = True
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

    def __rangeMapRule(self, struct):
        isBottom = False
        const = range
        paramList = [struct.start, struct.stop, struct.step]
        paramMapIdx = [0, 1]
        ifExpand = True
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

    def __strMapRule(self, struct):
        if len(struct) <= 1 and self.passStr is True:
            isBottom = True
        else:
            isBottom = False
            self.passStr = True
        const = ''.join
        paramList = [x for x in struct]
        paramMapIdx = range(len(paramList))
        ifExpand = False
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)

'''
# testing code
if __name__ == '__main__':
    # single level test instances
    sList1 = [1, 2, 3]
    sTuple1 = (1, 2, 3)
    sDict1 = {1: 2, 2: 3, 3: 4}
    sSlice1 = slice(None, 10, 2)
    sRange1 = range(10)
    sStr1 = '123'

    sMixed1 = [[(1, 2, 4), (4, 5)], [(6, 7, 8), '91011']]

    # double level test instances
    sList2 = [[1, 2], [3, 4], [5, 6, 7]]
    sTuple2 = ((1, 2), (3, 4), (5, 6, 7))
    sDict2 = {1: {1: 1, 2: 2}, 2: {1: 3, 2: 4, 3: 5}}
    sSlice2 = [slice(None, 10 ,2), slice(1, 3, None), slice(2, None, None)]
    sRange2 = (range(3), range(1, 5), range(2, 10, 3))
    sStr2 = ['12', '34', '567']
    sMixed = [(1, 2), [3, 4, 5], {6: 6, 7: 7}, range(3), slice(None, 10, 2)]

    # two functions
    fun1 = lambda x: x+1
    fun2 = lambda x: str(int(x)+1)
    fun3 = lambda x: x+2
    fun4 = lambda x: x[0]

    # gmap objects
    mp1 = GMap()
    mp2 = GMap(intoStr=True)
    mp3 = GMap(recDepth=1)
    mp4 = GMap(recDepth=1, intoStr=True)
    mp5 = GMap(recDepth=2)
    mp6 = GMap(recDepth=2, intoStr=True)
    
    # test auto map
    print(mp1.gMap(fun1, sList1))
    print(mp1.gMap(fun1, sTuple1))
    print(mp1.gMap(fun1, sDict1))
    print(mp1.gMap(fun1, sSlice1))
    print(mp1.gMap(fun1, sRange1))
    print(mp2.gMap(fun2, sStr1))

    print(mp1.gMap(fun1, sList2))
    print(mp1.gMap(fun1, sTuple2))
    print(mp1.gMap(fun1, sDict2))
    print(mp1.gMap(fun1, sSlice2))
    print(mp1.gMap(fun1, sRange2))
    print(mp2.gMap(fun2, sStr2))
    
    print(mp1.gMap(fun1, sMixed))

    print(mp5.gMap(fun4, sMixed1))

    # test depth specified map
    print(mp3.gMap(fun1, sList1))
    print(mp3.gMap(fun1, sTuple1))
    print(mp3.gMap(fun1, sDict1))
    print(mp3.gMap(fun1, sSlice1))
    print(mp3.gMap(fun1, sRange1))
    print(mp4.gMap(fun2, sStr1))

    print(mp5.gMap(fun1, sList2))
    print(mp5.gMap(fun1, sTuple2))
    print(mp5.gMap(fun1, sDict2))
    print(mp5.gMap(fun1, sSlice2))
    print(mp5.gMap(fun1, sRange2))
    print(mp6.gMap(fun2, sStr2))
    
    # multiple levels, non-homogeneous structures
    sBulk = [([1, 2], (3, 4, 5)), [{1: 6, 2: 7}, range(10), slice(None, 6, 2)]]
    print(mp1.gMap(fun1, sBulk))
    print(mp1.gMap(fun3, sBulk))

    # instances should fail
    # print(mp1.gMap(fun2, sStr1))
    # print(mp5.gMap(fun1, sList1))
    # print(mp3.gMap(fun1, sList2))

    # self defined
    class MSet:
        def __init__(self, lst):
            self.elems = lst

        def __repr__(self):
            return('MSet' + str(self.elems) + '')

        def __getitem__(self, idx):
            if type(idx) is int:
                return self.elems[idx]
            else:
                return MSet(self.elems[idx])

        def toList(self):
            return self.elems

    # test multiset
    mset = MSet([1, 2, 3])
    print(mset)
    print(mset[1])
    print(mset[0:2])
    print(mset.toList())

    # define mapRules
    def msetMapRule(mset):
        isBottom = False
        const = MSet
        paramList = mset.toList()
        paramMapIdx = range(len(paramList))
        ifExpand = False
        projFunc = lambda x: x
        liftFunc = lambda x, res: res
        return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)
    
    # define recursive structure
    mset0 = MSet([1,2])
    mset1 = MSet([3,4])
    mset = MSet([mset0, mset1])
   
    # define nonhomo recursive structure
    mtuple = (mset0, mset1)

    mp7 = GMap()
    mp7.regStructType(MSet, msetMapRule)
    
    print(mp7.gMap(fun1, mset))
    print(mp7.gMap(fun1, mtuple))
'''
