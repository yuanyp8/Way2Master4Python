

`shutil`模块提供了一系列对文件和文件集合的高阶操作。 特别是提供了一些支持文件拷贝和删除的函数

## 目录和文件操作

### shutil.copyfileobj(*fsrc*, *fdst*[, *length*])

将文件类对象 *fsrc* 的内容拷贝到文件类对象 *fdst*。 整数值 *length* 如果给出则为缓冲区大小。 特别地， *length* 为负值表示拷贝数据时不对源数据进行分块循环处理；默认情况下会分块读取数据以避免不受控制的内存消耗。 请注意如果 *fsrc* 对象的当前文件位置不为 0，则只有从当前文件位置到文件末尾的内容会被拷贝。

- 自己写一个复制文件对象

```Python
with open('test1', mode='w+') as f1:
    f1.write("My name is test1")
    f1.flush()
    f1.seek(0)
    with open('test2', mode='w+') as f2:
        f2.write(f1.read())

for i in ['test1', 'test2']:
    with open(i) as f:
        print(i, f.read())

#结果如下
test1 My name is test1
test2 My name is test1
```

#### copyfileobj源码

```Python
def copyfileobj(fsrc, fdst, length=16*1024):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
```

使用一下

```Python
from shutil import copyfileobj
with open('test1', mode='wb+') as f1:
    f1.write('My name is test1'.encode())
    f1.seek(0)
    with open('test2', mode='wb+') as f2:
        copyfileobj(f1, f2)


for i in ['test1', 'test2']:
    with open(i) as f:
        print(f.read())

# 结果如下
My name is test1
My name is test1
```

### shutil.copyfile(*src*, *dst*, *, *follow_symlinks=True*)

将名为 *src* 的文件的内容（不包括元数据）拷贝到名为 *dst* 的文件并以尽可能**高效**的方式返回 *dst*。 *src* 和 *dst* 均为路径类对象或以字符串形式给出的路径名。

*dst* 必须是完整的目标文件名；对于接受目标目录路径的拷贝请参见 `copy()`。 如果 *src* 和 *dst* 指定了同一个文件，则将引发 `SameFileError`。

目标位置必须是可写的；否则将引发 `OSError` 异常。 如果 *dst* 已经存在，它将被替换。 特殊文件如字符或块设备以及管道无法用此函数来拷贝。

如果 *follow_symlinks* 为假值且 *src* 为符号链接，则将创建一个新的符号链接而不是拷贝 *src* 所指向的文件。

引发一个 审计事件`shutil.copyfile` 附带参数 `src`, `dst`。

*在 3.3 版更改:* 曾经是引发 `IOError`而不是 `OSError`。 增加了 *follow_symlinks* 参数。 现在是返回 *dst*。

*在 3.4 版更改:* 引发 `SameFileError`而不是 `Error`。 由于前者是后者的子类，此改变是向后兼容的。

*在 3.8 版更改:* 可能会在内部使用平台专属的快速拷贝系统调用以更高效地拷贝文件。

```Python
def copyfile(src, dst, *, follow_symlinks=True):
    """Copy data from src to dst in the most efficient way possible.

    If follow_symlinks is not set and src is a symbolic link, a new
    symlink will be created instead of copying the file it points to.

    """
    sys.audit("shutil.copyfile", src, dst)

    if _samefile(src, dst):
        raise SameFileError("{!r} and {!r} are the same file".format(src, dst))

    file_size = 0
    for i, fn in enumerate([src, dst]):
        try:
            st = _stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if stat.S_ISFIFO(st.st_mode):
                fn = fn.path if isinstance(fn, os.DirEntry) else fn
                raise SpecialFileError("`%s` is a named pipe" % fn)
            if _WINDOWS and i == 0:
                file_size = st.st_size

    if not follow_symlinks and _islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            # macOS
            if _HAS_FCOPYFILE:
                try:
                    _fastcopy_fcopyfile(fsrc, fdst, posix._COPYFILE_DATA)
                    return dst
                except _GiveupOnFastCopy:
                    pass
            # Linux
            elif _USE_CP_SENDFILE:
                try:
                    _fastcopy_sendfile(fsrc, fdst)
                    return dst
                except _GiveupOnFastCopy:
                    pass
            # Windows, see:
            # https://github.com/python/cpython/pull/7160#discussion_r195405230
            elif _WINDOWS and file_size > 0:
                _copyfileobj_readinto(fsrc, fdst, min(file_size, COPY_BUFSIZE))
                return dst

            copyfileobj(fsrc, fdst)

    return dst
```


- 核心代码如下

```Python
       with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:  # 模式为二进制
             elif _USE_CP_SENDFILE:
                try:
                    _fastcopy_sendfile(fsrc, fdst)
                    return dst
                except _GiveupOnFastCopy:
                    pass
```

- 可以看看_samefile()实现逻辑

```Python
def _samefile(src, dst):
    # Macintosh, Unix.
    if isinstance(src, os.DirEntry) and hasattr(os.path, 'samestat'):
        try:
            return os.path.samestat(src.stat(), os.stat(dst))
        except OSError:
            return False

    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))
```

上面的拷贝是没有复制权限

验证下

```python
>>> from pathlib import Path
>>> import shutil
>>> with Path('./t1').open(mode='wb+') as f:
...     f.write('Hello t1'.encode())
...
8
>>> Path('t1').chmod(0o777)
>>> shutil.copyfile('./t1', 't2')
't2'
>>> with Path('t2').open('r+') as f:
...     f.read()
...
'Hello t1'

>>> exit()
[root@localhost python]<20210302 14:59:26># ll
total 8
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rw------- 1 root root 8 Mar  2 14:59 t2
```



### shutil.copymode(*src*, *dst*, *, *follow_symlinks=True*)

从 *src* 拷贝权限位到 *dst*。 文件的内容、所有者和分组将不受影响。 *src* 和 *dst* 均为路径类对象或字符串形式的路径名。 如果 *follow_symlinks* 为假值，并且 *src* 和 *dst* 均为符号链接，`copymode()` 将尝试修改 *dst* 本身的模式（而非它所指向的文件）。 此功能并不是在所有平台上均可用； 如果 `copymode()`无法修改本机平台上的符号链接，而它被要求这样做，它将不做任何操作即返回。

引发一个 审计事件]`shutil.copymode` 附带参数 `src`, `dst`。

*在 3.3 版更改:* 加入 *follow_symlinks* 参数。

```Python
def copymode(src, dst, *, follow_symlinks=True):
    """Copy mode bits from src to dst.

    If follow_symlinks is not set, symlinks aren't followed if and only
    if both `src` and `dst` are symlinks.  If `lchmod` isn't available
    (e.g. Linux) this method does nothing.

    """
    sys.audit("shutil.copymode", src, dst)

    if not follow_symlinks and _islink(src) and os.path.islink(dst):
        if hasattr(os, 'lchmod'):
            stat_func, chmod_func = os.lstat, os.lchmod
        else:
            return
    else:
        stat_func, chmod_func = _stat, os.chmod

    st = stat_func(src)
    chmod_func(dst, stat.S_IMODE(st.st_mode))

```



```Python
>>> from shutil import copymode
>>> from pathlib import Path
>>> Path('t1').stat()
os.stat_result(st_mode=33279, st_ino=101753955, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614668362, st_mtime=1614667812, st_ctime=1614668334)
>>> Path('t2').stat()
os.stat_result(st_mode=33152, st_ino=102003463, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614667908, st_mtime=1614668362, st_ctime=1614668362)
>>> copymode('t1', 't2')
>>> Path('t2').stat()
os.stat_result(st_mode=33279, st_ino=102003463, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614667908, st_mtime=1614668362, st_ctime=1614668447)
>>> exit()
[root@localhost python]<20210302 15:01:19># ll
total 8
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rwxrwxrwx 1 root root 8 Mar  2 14:59 t2

```


上面的copymode单独拷贝了权限，并没有stat的相关信息

### shutil.copystat(*src*, *dst*, *, *follow_symlinks=True*)

从 *src* 拷贝权限位、最近访问时间、最近修改时间以及旗标到 *dst*。 在 Linux上，`copystat()`还会在可能的情况下拷贝“扩展属性”。 文件的内容、所有者和分组将不受影响。 *src* 和 *dst* 均为路径类对象或字符串形式的路径名。

如果 *follow_symlinks* 为假值，并且 *src* 和 *dst* 均指向符号链接，`copystat()`将作用于符号链接本身而非该符号链接所指向的文件 — 从 *src* 符号链接读取信息，并将信息写入 *dst* 符号链接。

```Python
[root@localhost python]<20210302 15:15:41># ll
total 8
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rw------- 1 root root 8 Mar  2 14:59 t2

>>> from shutil import copystat
>>> copystat('t1', 't2')
>>> Path('t1').stat()
os.stat_result(st_mode=33279, st_ino=101753955, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614668362, st_mtime=1614667812, st_ctime=1614668334)
>>> Path('t2').stat()
os.stat_result(st_mode=33279, st_ino=102003463, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614668362, st_mtime=1614667812, st_ctime=1614669404)
```

### shutil.copy(*src*, *dst*, *, *follow_symlinks=True*)

将文件 *src* 拷贝到文件或目录 *dst*。 *src* 和 *dst* 应为 路径类对象或字符串。 如果 *dst* 指定了一个目录，文件将使用 *src* 中的基准文件名拷贝到 *dst* 中。 将返回新创建文件所对应的路径。

如果 *follow_symlinks* 为假值且 *src* 为符号链接，则 *dst* 也将被创建为符号链接。 如果 *follow_symlinks* 为真值且 *src* 为符号链接，*dst* 将成为 *src* 所指向的文件的一个副本。

`copy()`会拷贝文件数据和文件的权限模式 。 其他元数据，例如文件的创建和修改时间不会被保留。 要保留所有原有的元数据，请改用 `copy2()`。

```Python
>>> import shutil
>>> shutil.copy('t2', 't3')
't3'
>>> exit()
[root@localhost python]<20210302 15:22:03># ll
total 12
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t2
-rwxrwxrwx 1 root root 8 Mar  2 15:21 t3


>>> from pathlib import Path
>>> Path('t2').stat()
os.stat_result(st_mode=33279, st_ino=102003463, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614669718, st_mtime=1614667812, st_ctime=1614669404)
>>> Path('t3').stat()
os.stat_result(st_mode=33279, st_ino=102295023, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614669718, st_mtime=1614669718, st_ctime=1614669718)

# 可以看到了只执行了copyfile 和copymode
```

### shutil.copy2(*src*, *dst*, *, *follow_symlinks=True*)

类似于 `copy()`，区别在于 `copy2()`还会尝试保留文件的元数据。

当 *follow_symlinks* 为假值且 *src* 为符号链接时，`copy2()` 会尝试将来自 *src* 符号链接的所有元数据拷贝到新创建的 *dst* 符号链接。 但是，此功能不是在所有平台上均可用。 在此功能部分或全部不可用的平台上，`copy2()` 将尽量保留所有元数据；`copy2()`一定不会由于无法保留文件元数据而引发异常。

`copy2()`会使用 `copystat()`来拷贝文件元数据。 请参阅 `copystat()`了解有关修改符号链接元数据的平台支持的更多信息。

```Python
>>> shutil.copy2('t2', 't4')
't4'
>>> Path('t2').stat()
os.stat_result(st_mode=33279, st_ino=102003463, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614669718, st_mtime=1614667812, st_ctime=1614669404)
>>> Path('t4').stat()
os.stat_result(st_mode=33279, st_ino=102017836, st_dev=2051, st_nlink=1, st_uid=0, st_gid=0, st_size=8, st_atime=1614669718, st_mtime=1614667812, st_ctime=1614670049)
```

### shutil.copytree

shutil.copytree(*src*, *dst*, *symlinks=False*, *ignore=None*, *copy_function=copy2*, *ignore_dangling_symlinks=False*, *dirs_exist_ok=False*)copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False)

- 将以 *src* 为根起点的整个目录树拷贝到名为 *dst* 的目录并返回目标目录。 *dirs_exist_ok* 指明是否要在 *dst* 或任何丢失的父目录已存在的情况下引发异常。

- 目录的权限和时间会通过 `copystat()`来拷贝，单个文件则会使用 `copy2()` 来拷贝
- 如果 *symlinks* 为真值，源目录树中的符号链接会在新目录树中表示为符号链接，并且原链接的元数据在平台允许的情况下也会被拷贝；如果为假值或省略，则会将被链接文件的内容和元数据拷贝到新目录树。
- 当 *symlinks* 为假值时，如果符号链接所指向的文件不存在，则会在拷贝进程的末尾将一个异常添加到 `Error`异常中的错误列表。 如果你希望屏蔽此异常那就将可选的 *ignore_dangling_symlinks* 旗标设为真值。 请注意此选项在不支持 `os.symlink()`的平台上将不起作用。
- 如果给出了 *copy_function*，它必须是一个将被用来拷贝每个文件的可调用对象。 它在被调用时会将源路径和目标路径作为参数传入。 默认情况下，`copy2()` 将被使用，但任何支持同样签名（与 `copy()`一致）都可以使用。

- src、dst必须是目录
- src必须存在
- dst必须不存在


```Python
[root@localhost test]<20210302 15:46:17># ll
total 4
drwx------ 2 qtdev users 46 Mar  2 15:27 python
-rw------- 1 root  root  11 Mar  2 14:24 test.py
[root@localhost test]<20210302 15:46:17># ll python/
total 16
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t2
-rwxrwxrwx 1 root root 8 Mar  2 15:21 t3
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t4

>>> import shutil
>>> shutil.copytree('./python', 'python1')
'python1'
>>> exit()
[root@localhost test]<20210302 15:47:32># ll
total 4
drwx------ 2 qtdev users 46 Mar  2 15:27 python
drwx------ 2 root  root  46 Mar  2 15:27 python1
-rw------- 1 root  root  11 Mar  2 14:24 test.py
[root@localhost test]<20210302 15:47:34># ll python1
total 16
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t2
-rwxrwxrwx 1 root root 8 Mar  2 15:21 t3
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t4


```

### shutil.rmtree(*path*, *ignore_errors=False*, *onerror=None*)

删除一个完整的目录树；*path* 必须指向一个目录（但不能是一个目录的符号链接）。 如果 *ignore_errors* 为真值，删除失败导致的错误将被忽略；如果为假值或是省略，此类错误将通过调用由 *onerror* 所指定的处理程序来处理，或者如果此参数被省略则将引发一个异常。


```Python
import shutil
shutil.rmtree('/')
# 等同 rm -rf /
```

### shutil.move(*src*, *dst*, *copy_function=copy2*)

递归地将一个文件或目录 (*src*) 移至另一位置 (*dst*) 并返回目标位置。

如果目标是已存在的目录，则 *src* 会被移至该目录下。 如果目标已存在但不是目录，它可能会被覆盖，具体取决于 `os.rename()` 的语义。

```Python
>>> import shutil
>>> shutil.move('b','bb')
'bb'
>>> shutil.move('a','acc/a')
'acc/a'
```

### shutil.disk_usage(*path*)

返回给定路径的磁盘使用统计数据，形式为一个 named tuple，其中包含 *total*, *used* 和 *free* 属性，分别表示总计、已使用和未使用空间的字节数。 *path* 可以是一个文件或是一个目录。

```python
>>> import shutil
>>> from pathlib import Path
>>> shutil.disk_usage(Path(''))
usage(total=42402574336, used=27320287232, free=15082287104)
```

### shutil.chown(*path*, *user=None*, *group=None*)

修改给定 *path* 的所有者 *user* 和/或 *group*。

*user* 可以是一个系统用户名或 uid；*group* 同样如此。 要求至少有一个参数。

```python
[root@localhost python]<20210302 16:04:35># ls -lh t1
-rwxrwxrwx 1 root root 8 Mar  2 14:50 t1
    
>>> import shutil
>>> from pathlib import Path
>>> shutil.chown(Path('./t1'), 'dev', 'dev')
>>> exit()
[root@localhost python]<20210302 16:06:19># ls -lh t1
-rwxrwxrwx 1 dev dev 8 Mar  2 14:50 t1
```

