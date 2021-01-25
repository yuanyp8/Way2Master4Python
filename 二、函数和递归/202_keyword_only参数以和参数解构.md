## keyword-only参数

### 定义

Python3.X将函数头部的顺序规则一般化，以允许我们指定keyword-only参数---即必须只按照关键字传入并永远不会被基于位置参数来填充的参数。

从语法上讲，keyword-only参数编写为出现在参数列表中*args之后的有名参数。所有这些参数都必须在调用中使用关键字语法来传递。

下面就是一个keyword-only参数

```python
def keyword(x,y,aa='aa',*arg,z):
    print("{} is a keyword-only argument".format(z))
    return aa
s = keyword(3,4,123,45,6,7,5,3,5,6,z='abc')
print(s)
```

### 原理解析

先来看个例子

```python
>>> def fn(x,*arg):
        print(x,arg)

>>> fn(1,2,3,4,5)
1 (2, 3, 4, 5)
```

可以看到`*`起到贪婪模式作用，如果想在`*arg`后面加一个形参，该怎么做？
位置参数肯定是不支持的，因为前面是贪婪模式，**会吞并所有位置参数**

```python
>>> def fn1(x,*arg,y):
	print(x,arg,y)

>>> fn1(1,2,3,4,5,6,7,8,8)
Traceback (most recent call last):
  File "<pyshell#167>", line 1, in <module>
    fn1(1,2,3,4,5,6,7,8,8)
TypeError: fn1() missing 1 required keyword-only argument: 'y'
```


所以，* arg后面只能是关键字参数！！！

```python
>>> def fn2(x,*arg,y):
	print(x,arg,y)

>>> fn2(1,2,3,4,5,6,7,8,y=2)
1 (2, 3, 4, 5, 6, 7, 8) 2
>>> fn2(x=2,y=2)
2 () 2
```

这就是KeyWord-only参数


>只会对*arg存在，** kwarg不考虑，因为 kwarg不能接任何参数

假如你觉得*args意义不大，可以如下使用

```python
>>> def fn4(x,y,*,z):
	print(x,y,z)
>>> fn4(1,2,z=4)
1 2 4
```


### 形参的混合使用

#### 可变位置参数和缺省参数

```python
>>> def aa(*args,x=3):
	print(args,x)

>>> aa(x=5)
() 5
#这里直接使用关键字传参即可
```

#### 位置参数、可变参数、缺省参数

```python
>>> def ab(x,*args,y=4):
	print(x,args,y)

>>> ab(x=4,y=5)
4 () 5
>>> ab(4,3,4,5,6,7,y=5)
4 (3, 4, 5, 6, 7) 5
>>> ab(4)
4 () 4
```

### 规约

- 定义最常用参数作为普通参数，可不提供缺省值，必须由用户提供，注意参数的顺序，最常用的先定义
- 将必须使用名称的才能使用的参数，定义为keyword-only参数，要求必须使用关键字参数
- 如果函数有很多参数，无法逐一定义，可使用可变参数。如果要知道这些参数的意义，则使用可变关键字参数



## 解构

前面都是封装，下面看看解构

### 实参解构

对于定义好的如下函数

```python
>>> def add(x,y):
	print(x,y)
	return x+y

>>> add(2,3)
2 3
5
```

我们也可以这样操作

```python
>>> add(*[2,3])
2 3
5
>>> add(*{2,3})
2 3
5
>>> add(*(2,3))
2 3
5
```

### 字典解构

```python
>>> add(*{"a":1,"b":2})
a b
'ab'
>>> add(*{"a":1,"b":2}.keys())
a b

#利用**
>>> add(**{"x":2,"y":3})
2 3
5
```

### 总结

- 在给函数提供实参的时候，可以在可迭代对象前面使用*或者**来进行解构，提取出其中所有元素作为函数的实参
- 使用*解构成位置传参
- 使用**解构成关键字传参
- 提取出的元素数目要和传参一一对应


## 练习

### 练习1

 编写一个函数，能够至少接受两个参数，返回最小值和最大值

```python
def max_min(arg,arg1,*args):
    print('Max Num is:',max(arg,arg1,*args))
    print('Min Num is:',min(arg,arg,*args))

max_min(2,3,4,6,3,1,8)
```

不使用max,min函数

```python
def max_min(x,y,*args):
    if len(args) != 0:
        sett = (x,y) + args
        max_ = 0
        min_ = -1
        for i,j in enumerate(sett):
            if j > sett[max_] and j != sett[max_]:
                max_ = i
            if sett[-1-i] < sett[min_] and sett[-1-i] != sett[min_]:
                min_ = -1-i
        print(sett[max_],sett[min_])
    else:
        print(x,y) if x > y else print(y,x)
```

### 练习2

完成一个函数，可以接受输入的多个数，每一次都能返回到目前为止的最大数、最小值

```python
def fn():
    max_ = None
    min_ = None
    while True:
        i = input(">>>")
        nums = i.replace(",", " ").split()
        # lst = [int(x) for x in nums]
        for i in nums:
            n = int(i)
            if max_ is None:
                max_ = n
                min_ = n
            if max_ < n:
                max_ = n
            if min_ > n:
                min_ = n
        print(max_,min_)
```