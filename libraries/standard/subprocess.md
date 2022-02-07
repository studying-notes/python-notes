---
date: 2021-03-06T20:18:10+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "subprocess - 子进程管理"  # 文章标题
url:  "posts/python/libraries/standard/subprocess"  # 设置网页永久链接
tags: [ "python", "standard", "subprocess" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

https://docs.python.org/zh-cn/3/library/subprocess.html

subprocess 模块允许你生成新的进程，连接它们的输入、输出、错误管道，并且获取它们的返回码。

可以替代以下旧模块实现：

```
os.system
os.spawn*
```

## subprocess.run()

推荐的调用子进程的方式是在任何它支持的用例中使用 run() 函数

```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None, **other_popen_kwargs)
```

运行被 arg 描述的指令。等待指令完成，然后返回一个 CompletedProcess 实例。

如果 capture_output 设为 true，stdout 和 stderr 将会被捕获。在使用时，内置的 Popen 对象将自动用 stdout=PIPE 和 stderr=PIPE 创建。stdout 和 stderr 参数不应当与 capture_output 同时提供。如果你希望捕获并将两个流合并在一起，使用 stdout=PIPE 和 stderr=STDOUT 来代替 capture_output。

timeout 参数将被传递给 Popen.communicate()。如果发生超时，子进程将被杀死并等待。 TimeoutExpired 异常将在子进程中断后被抛出。

input 参数将被传递给 Popen.communicate() 以及子进程的标准输入。 如果使用此参数，它必须是一个字节序列。 如果指定了 encoding 或 errors 或者将 text 设置为 True，那么也可以是一个字符串。 当使用此参数时，在创建内部 Popen 对象时将自动带上 stdin=PIPE，并且不能再手动指定 stdin 参数。

如果 check 设为 True, 并且进程以非零状态码退出, 一个 CalledProcessError 异常将被抛出. 这个异常的属性将设置为参数, 退出码, 以及标准输出和标准错误, 如果被捕获到.

如果 encoding 或者 error 被指定, 或者 text 被设为 True, 标准输入, 标准输出和标准错误的文件对象将通过指定的 encoding 和 errors 以文本模式打开, 否则以默认的 io.TextIOWrapper 打开. universal_newline 参数等同于 text 并且提供了向后兼容性. 默认情况下, 文件对象是以二进制模式打开的.

如果 env 不是 None, 它必须是一个字典, 为新的进程设置环境变量; 它用于替换继承的当前进程的环境的默认行为. 它将直接被传递给 Popen.

例如:

```python
>>> subprocess.run(["ls", "-l"])  # doesn't capture output
CompletedProcess(args=['ls', '-l'], returncode=0)

>>> subprocess.run("exit 1", shell=True, check=True)
Traceback (most recent call last):
  ...
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

>>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')
```

### class subprocess.CompletedProcess

> run() 的返回值, 代表一个进程已经结束.

- args 被用作启动进程的参数. 可能是一个列表或字符串.
- returncode 子进程的退出状态码. 通常来说, 一个为 0 的退出码表示进程运行正常. 一个负值 -N 表示子进程被信号 N 中断 (仅 POSIX).
- stdout 从子进程捕获到的标准输出. 一个字节序列, 或一个字符串, 如果 run() 是设置了 encoding, errors 或者 text=True 来运行的. 如果未有捕获, 则为 None. 如果你通过 stderr=subprocess.STDOUT 运行, 标准输入和标准错误将被组合在一起, 并且 stderr` 将为 None.
- stderr 捕获到的子进程的标准错误. 一个字节序列, 或者一个字符串, 如果 run() 是设置了参数 encoding, errors 或者 text=True 运行的. 如果未有捕获, 则为 None.
- check_returncode() 如果 returncode 非零, 抛出 CalledProcessError.

## Popen 构造函数

run()

```python
def run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs):
    """Run command with arguments and return a CompletedProcess instance.

    The returned instance will have attributes args, returncode, stdout and
    stderr. By default, stdout and stderr are not captured, and those attributes
    will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them.

    If check is True and the exit code was non-zero, it raises a
    CalledProcessError. The CalledProcessError object will have the return code
    in the returncode attribute, and output & stderr attributes if those streams
    were captured.

    If timeout is given, and the process takes too long, a TimeoutExpired
    exception will be raised.

    There is an optional argument "input", allowing you to
    pass bytes or a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's "stdin" argument, as
    it will be used internally.

    By default, all communication is in bytes, and therefore any "input" should
    be bytes, and the stdout and stderr will be bytes. If in text mode, any
    "input" should be a string, and stdout and stderr will be strings decoded
    according to locale encoding, or by "encoding" if set. Text mode is
    triggered by setting any of text, encoding, errors or universal_newlines.

    The other arguments are the same as for the Popen constructor.
    """
    if input is not None:
        if kwargs.get('stdin') is not None:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = PIPE

    if capture_output:
        if kwargs.get('stdout') is not None or kwargs.get('stderr') is not None:
            raise ValueError('stdout and stderr arguments may not be used '
                             'with capture_output.')
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE

    with Popen(*popenargs, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except TimeoutExpired as exc:
            process.kill()
            if _mswindows:
                # Windows accumulates the output in a single blocking
                # read() call run on child threads, with the timeout
                # being done in a join() on those threads.  communicate()
                # _after_ kill() is required to collect that and add it
                # to the exception.
                exc.stdout, exc.stderr = process.communicate()
            else:
                # POSIX _communicate already populated the output so
                # far into the TimeoutExpired exception.
                process.wait()
            raise
        except:  # Including KeyboardInterrupt, communicate handled that.
            process.kill()
            # We don't call process.wait() as .__exit__ does that for us.
            raise
        retcode = process.poll()
        if check and retcode:
            raise CalledProcessError(retcode, process.args,
                                     output=stdout, stderr=stderr)
    return CompletedProcess(process.args, retcode, stdout, stderr)
```

```python
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, group=None, extra_groups=None, user=None, umask=-1, encoding=None, errors=None, text=None)
```

在一个新的进程中执行子程序。在 POSIX，此类使用类似于 os.execvp() 的行为来执行子程序。在 Windows，此类使用了 Windows CreateProcess() 函数。 Popen 的参数如下：

args 应当是一个程序参数的序列或者是一个单独的字符串或 path-like object。 默认情况下，如果 args 是序列则要运行的程序为 args 中的第一项。 如果 args 是字符串，则其解读依赖于具体平台，如下所述。 请查看 shell 和 executable 参数了解其与默认行为的其他差异。 除非另有说明，否则推荐以序列形式传入 args。

向外部函数传入序列形式参数的一个例子如下:

```python
Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])
```

在 POSIX，如果 args 是一个字符串，此字符串被作为将被执行的程序的命名或路径解释。但是，只有在不传递任何参数给程序的情况下才能这么做。

将 shell 命令拆分为参数序列的方式可能并不很直观，特别是在复杂的情况下。 shlex.split() 可以演示如何确定 args 适当的拆分形式:

```python
>>> import shlex, subprocess
>>> command_line = input()
/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
>>> args = shlex.split(command_line)
>>> print(args)
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
>>> p = subprocess.Popen(args) # Success!
```

在 Windows，如果 args 是一个序列，他将通过一个在 在 Windows 上将参数列表转换为一个字符串 描述的方式被转换为一个字符串。这是因为底层的 CreateProcess() 只处理字符串。

参数 shell （默认为 False）指定是否使用 shell 执行程序。如果 shell 为 True，更推荐将 args 作为字符串传递而非序列。

在 POSIX，当 shell=True， shell 默认为 /bin/sh。如果 args 是一个字符串，此字符串指定将通过 shell 执行的命令。这意味着字符串的格式必须和在命令提示符中所输入的完全相同。这包括，例如，引号和反斜杠转义包含空格的文件名。如果 args 是一个序列，第一项指定了命令，另外的项目将作为传递给 shell （而非命令） 的参数对待。也就是说， Popen 等同于:

```python
Popen(['/bin/sh', '-c', args[0], args[1], ...])
```

在 Windows，使用 shell=True，环境变量 COMSPEC 指定了默认 shell。在 Windows 你唯一需要指定 shell=True 的情况是你想要执行内置在 shell 中的命令（例如 dir 或者 copy）。在运行一个批处理文件或者基于控制台的可执行文件时，不需要 shell=True。

bufsize 将在 open() 函数创建了 stdin/stdout/stderr 管道文件对象时作为对应的参数供应:

- 0 表示不使用缓冲区 （读取与写入是一个系统调用并且可以返回短内容）
- 1 表示行缓冲（只有 universal_newlines=True 时才有用，例如，在文本模式中）
- 任何其他正值表示使用一个约为对应大小的缓冲区
- 负的 bufsize （默认）表示使用系统默认的 io.DEFAULT_BUFFER_SIZE。

executable 参数指定一个要执行的替换程序。这很少需要。当 shell=True， executable 替换 args 指定运行的程序。但是，原始的 args 仍然被传递给程序。大多数程序将被 args 指定的程序作为命令名对待，这可以与实际运行的程序不同。在 POSIX， args 名作为实际调用程序中可执行文件的显示名称，例如 ps。如果 shell=True，在 POSIX， executable 参数指定用于替换默认 shell /bin/sh 的 shell。

stdin, stdout 和 stderr 分别指定被运行的程序的标准输入、输出和标准错误的文件句柄。合法的值有 PIPE ， DEVNULL ， 一个存在的文件描述符（一个正整数），一个存在的 文件对象 以及 None。 PIPE 表示应创建一个新的对子进程的管道。 DEVNULL 表示使用特殊的 os.devnull 文件。使用默认的 None，则不进行成定向；子进程的文件流将继承自父进程。另外， stderr 可设为 STDOUT，表示应用程序的标准错误数据应和标准输出一同捕获。

如果 env 不为 None，则必须为一个为新进程定义了环境变量的字典；这些用于替换继承的当前进程环境的默认行为。如果指定， env 必须提供所有被子进程需求的变量。在 Windows，为了运行一个 side-by-side assembly ，指定的 env 必须 包含一个有效的 SystemRoot。

如果 encoding 或 errors 被指定，或者 text 为 true，则文件对象 stdin, stdout 和 stderr 将会以指定的编码和 errors 以文本模式打开，如同 常用参数 所述。 universal_newlines 参数等同于 text 并且提供向后兼容性。默认情况下，文件对象都以二进制模式打开。

Popen 对象支持通过 with 语句作为上下文管理器，在退出时关闭文件描述符并等待进程:

```python
with Popen(["ifconfig"], stdout=PIPE) as proc:
    log.write(proc.stdout.read())
```

不像一些其他的 popen 功能，此实现绝不会隐式调用一个系统 shell。这意味着任何字符，包括 shell 元字符，可以安全地被传递给子进程。如果 shell 被明确地调用，通过 shell=True 设置，则确保所有空白字符和元字符被恰当地包裹在引号内以避免 shell 注入 漏洞就由应用程序负责了。

当使用 shell=True， shlex.quote() 函数可以作为在将被用于构造 shell 指令的字符串中转义空白字符以及 shell 元字符的方案。

## Popen 对象

### Popen.poll()

检查子进程是否已被终止。设置并返回 returncode 属性。否则返回 None。

### Popen.wait(timeout=None)

等待子进程被终止。设置并返回 returncode 属性。

如果进程在 timeout 秒后未中断，抛出一个 TimeoutExpired 异常，可以安全地捕获此异常并重新等待。

当 stdout=PIPE 或者 stderr=PIPE 并且子进程产生了足以阻塞 OS 管道缓冲区接收更多数据的输出到管道时，将会发生死锁。当使用管道时用 Popen.communicate() 来规避它。

### Popen.communicate(input=None, timeout=None)

与进程交互：将数据发送到 stdin。 从 stdout 和 stderr 读取数据，直到抵达文件结尾。 等待进程终止并设置 returncode 属性。 可选的 input 参数应为要发送到下级进程的数据，或者如果没有要发送到下级进程的数据则为 None。 如果流是以文本模式打开的，则 input 必须为字符串。 在其他情况下，它必须为字节串。

communicate() 返回一个 (stdout_data, stderr_data) 元组。如果文件以文本模式打开则为字符串；否则字节。

注意如果你想要向进程的 stdin 传输数据，你需要通过 stdin=PIPE 创建此 Popen 对象。类似的，要从结果元组获取任何非 None 值，你同样需要设置 stdout=PIPE 或者 stderr=PIPE。

如果进程在 timeout 秒后未终止，一个 TimeoutExpired 异常将被抛出。捕获此异常并重新等待将不会丢失任何输出。

如果超时到期，子进程不会被杀死，所以为了正确清理一个行为良好的应用程序应该杀死子进程并完成通讯。

```python
proc = subprocess.Popen(...)
try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
```

内存里数据读取是缓冲的，所以如果数据尺寸过大或无限，不要使用此方法。

### Popen.send_signal(signal)

将信号 signal 发送给子进程。如果进程已完成则不做任何操作。

> 在 Windows， SIGTERM 是一个 terminate() 的别名。 CTRL_C_EVENT 和 CTRL_BREAK_EVENT 可以被发送给以包含 CREATE_NEW_PROCESS 的 creationflags 形参启动的进程。

### Popen.terminate()

停止子进程。 在 POSIX 操作系统上，此方法会发送 SIGTERM 给子进程。 在 Windows 上则会调用 Win32 API 函数 TerminateProcess() 来停止子进程。

### Popen.kill()

杀死子进程。 在 POSIX 操作系统上，此函数会发送 SIGKILL 给子进程。 在 Windows 上 kill() 则是 terminate() 的别名。

terminate 信号可以被程序捕获，从而启动关闭进程，而不是突然中断，kill 是直接终止。

### Popen.args

args 参数传递给 Popen -- 一个程序参数的序列或者一个简单字符串。

### Popen.stdin

如果 stdin 参数为 PIPE，此属性是一个类似 open() 返回的可写的流对象。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，则此流是一个文本流，否则是字节流。如果 stdin 参数非 PIPE， 此属性为 None。

### Popen.stdout

如果 stdout 参数是 PIPE，此属性是一个类似 open() 返回的可读流。从流中读取子进程提供的输出。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，此流为文本流，否则为字节流。如果 stdout 参数非 PIPE，此属性为 None。

### Popen.stderr

如果 stderr 参数是 PIPE，此属性是一个类似 open() 返回的可读流。从流中读取子进程提供的输出。如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，此流为文本流，否则为字节流。如果 stderr 参数非 PIPE，此属性为 None。

> 使用 communicate() 而非 .stdin.write， .stdout.read 或者 .stderr.read 来避免由于任意其他 OS 管道缓冲区被子进程填满阻塞而导致的死锁。

### Popen.pid

子进程的进程号。注意如果你设置了 shell 参数为 True，则这是生成的子 shell 的进程号。

### Popen.returncode

此进程的退出码，由 poll() 和 wait() 设置（以及直接由 communicate() 设置）。一个 None 值 表示此进程仍未结束。

一个负值 -N 表示子进程被信号 N 中断 (仅 POSIX).

## 旧写法替代

### subprocess.call

```python
subprocess.run(...).returncode
```

### subprocess.check_call

```python
subprocess.run(..., check=True)
```

### subprocess.check_output

```python
subprocess.run(..., check=True, stdout=PIPE).stdout
```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```
