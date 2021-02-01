
  * [map()](#map)
     * [利用map函数构造字典](#利用map函数构造字典)
     * [map()双参数](#map双参数)
  * [filter](#filter)
  * [柯里化函数](#柯里化函数)
     * [例子](#例子)
## map()

map()就是通过自定义的方法得到映射后的数据,输出的惰性的迭代器  
类似于`x => xx`

```Python
x = map(lambda x: x*2, list(range(5)))
print(next(x))
print(next(x))
print(next(x))
```

### 利用map函数构造字典

- 字典解析式

```Python
>>> dct = {x:(x,x+1) for x in map(lambda i:i*2,range(10))}
>>> dct
{0: (0, 1), 2: (2, 3), 4: (4, 5), 6: (6, 7), 8: (8, 9), 10: (10, 11), 12: (12, 13), 14: (14, 15), 16: (16, 17), 18: (18, 19)}
```

- dict()

```Python
>>> d = dict(map(lambda x:(x,(x,x+1)),range(5)))
>>> d
{0: (0, 1), 1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5)}
```

- zip()

```Python
x = dict(zip(range(5),map(lambda x:x+1,range(5))))
print(x)
```

### map()双参数

```Python
a = list((map(lambda x,y:(x,y),range(5),range(1,6))))
print(a)
```

## filter

- 类似于map，前面写函数，用来过滤，后面写被执行对象

- 定义`filter(function, iterable)`
- 对可迭代对象进行遍历，返回一个迭代器
- function函数是一个参数的函数，且返回值应当是bool类型，或者其他返回值等效布尔值
- function函数如果是None，可迭代对象的每一个元素自身等效布尔值



```Python
a = list(filter(None,range(10))) # 比较值的bool值  
print(a)

b = list(filter(lambda x:None,range(10)))  # if fn(element): return element
print(b)

c = list(filter(lambda x:False,range(10)))
print(c)

d = list(filter(lambda x:x%3==0,range(15)))
print(d)

[1, 2, 3, 4, 5, 6, 7, 8, 9]
[]
[]
[0, 3, 6, 9, 12]
```

## 柯里化函数

- `z = f(x,y) => z = f(x)(y)`

- 指的将原来接受两个参数的函数变成新的接受一个参数的函数的过程。新的函数返回一个以原有第二个参数为参数的函数

### 例子

- 起始

```Python
def add(x,y):
    return x+y
a = add(4,5)
print(a)
```

- 变形

```Python
def fn1(x):
    def fn2(y):
        return x+y
    return fn2
print(fn1(1)(2))

def fn2(x):
    def fn3(y):
        def fn4(z):
            return x+y+z
        return fn4
    return fn3
print(fn2(2)(3)(4))

def fn(x,y):
    def fn1(z):
        return x+y+z
    return fn1
print(fn(1,2)(3))

def fnn(x):
    def fnnn(y,z):
        return x+y+z
    return fnnn

print(fnn(2)(3,4))

结果如下
3
9
6
9
```

