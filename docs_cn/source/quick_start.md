# Quick Start

Install with `pip`.

```bash
pip install advisor
```

Start the server.

```bash
advisor_admin server start
```

Go to `http://127.0.0.1:8000` in the browser.

Submit tuning jobs.

```bash
git clone --depth 1 https://github.com/tobegit3hub/advisor.git && cd ./advisor/

advisor run -f ./advisor_client/examples/python_function/config.json
```

Get result of jobs.

```bash
advisor study describe -s demo
```