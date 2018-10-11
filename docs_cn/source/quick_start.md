# 快速使用

使用`pip`安装。

```bash
pip install advisor
```

启动服务器。

```bash
advisor_admin server start
```

在浏览器打开`http://127.0.0.1:8000`。

提交调优任务。

```bash
git clone --depth 1 https://github.com/tobegit3hub/advisor.git && cd ./advisor/

advisor run -f ./advisor_client/examples/python_function/config.json
```

获取任务结果。

```bash
advisor study describe -s demo
```