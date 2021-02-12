


## reduce

- reduce: 顾名思义，就是减少的意思
- reduce(function,sequence[,imitial]) -> value
- 可迭代对象不能为空，初始值没提供就在可迭代对象取一个元素

先看个例子

```python
from functools import reduce

nums = [6,9,4,2,10,5,9,6,9]
print(nums)
print(sum(nums))
print(reduce(lambda x,y:x+y, nums))

结果如下
[6, 9, 4, 2, 10, 5, 9, 6, 9]
60
60
```


### 说明

```python
reduce(lambda x,y:x+y,range(5))
```

- x,y -- reduce必要的给出两个参数
- 将函数体的返回值(lambda就是函数体的计算结果)作为实参传入下一个迭代的x参数，
- 下一个迭代的y依序利用可迭代部分的下一个元素
- 计算结束后立即返回，也就是需要一个标识符来记住

>当然，reduce(xx),xx也可以是函数，只不过简单的函数可以使用lambda

## partial函数

偏函数，把函数部分的参数固定下来，相当于为部分的参数添加一个固定的默认值，形成一个新的函数并返回
从partial生成的新函数，是对原函数的封装


```python
from functools import wraps,update_wrapper,partial
import inspect

def add(x,y,z):
    return x+y+z

# 柯里化
def add(x):
    def inner(y,z):
        return x+y+z
    return inner
x=add(4)(5,6)
print(x)


def add(x,y,z):
    return x+y+z

# partial
def newfunc(x,y):
    return partial(add,x,y)
x = newfunc(3,4)(5)
print(x)

结果如下
15
12
```


### 举例演示


```python
from functools import wraps,update_wrapper,partial
import inspect

def add(x,y,z):
    return x+y+z

newfunc = partial(add,y=4)
print(inspect.signature(newfunc))

结果如下
(x, *, y=4, z)
```

>按结构来看，一旦中间的变量利用了关键字传参，那么y后面的只能是keyword-only传参


### 看下源码

```python
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

```

逐步分析


```python
def add(x,y,z):
    return x+y+z

 newfunc = partial(add,4)
 newfunc(y=5,z=6)
# 过程如下
= newfunc.func=add
  newfunc.args=4
  newfunc.keywords={}

= newkeywords={}
  newkeywords.update(y=5,z=6)
  newkeywords={"y":5,"z":6}

= add(4,y=5,z=6)

= 15
```

演示一个错误传参

```python
def add(x,y,z):
    return x+y+z

 newfunc = partial(add,y=4)

= newfunc.func=add
  newfunc.args=''
  newfunc.keywords={'y':4}

= newfunc(3,5)

= newkeywords = {'y':4}
  newkeywords.update({})

= add(3,5,y=4)
导致Error，传参失败

print(inspect.signature(newfunc))
(x, *, y=4, z)
可以看到，z必为keyword-only
```

## lru_cache

`functools.lru_cache(maxsize=128,typed=False)`

- least-recently-used装饰器，lru，最近最少使用，cache缓存
- 如果maxsize设置为None，则禁用LRU功能，并且缓存可以无限增长。当maxsize为2的幂次方时，LRU功能执行最好
- 如果typed设置为True，则不同类型的函数参数将单独缓存，例如：f(3)和f(3.0)将被视作具有不同结果的不同调用

>一般清理缓存的都是达到设定阈值后开始清理

### 使用

修改fibnacci

```python
import time,functools
@functools.lru_cache()
def fibonacci_seq(n):
    if n < 3:
        return 1
    return fibonacci_seq(n-1)+fibonacci_seq(n-2)


print(fibonacci_seq(35))
```





 