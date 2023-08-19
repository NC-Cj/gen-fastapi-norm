This is the structure of the template .

```text
│  .gitignore
│  LICENSE
│  main.py                         # 程序入口
│  requirements.txt                # 依赖
│
├─app
│  │  env.py                       # 环境变量初始化
│  │  middlewares.py               # 中间件，跨域等
│  │  __init__.py
│  │  
│  ├─controllers                   # 控制层
│  │      controllers.py
│  │
│  ├─dao                           # 数据库层
│  │      crud.py
│  │      postgresql.py
│  │      redis_.py
│  │
│  ├─docs                          # 业务文档（必要时按版本增加目录，例如/v1/README.md）
│  ├─logic                         # v1版本的api的业务逻辑
│  │  └─v1
│  │          user.py
│  │
│  ├─models                        # 模型目录，负责项目的数据存储部分
│  │      response.py              # 自定义响应模型
│  │      schema.py                # 数据库模型
│  │
│  ├─pkg                           # 自定义的工具类等
│  │  │  error.py                  # 自定义异常
│  │  │
│  │  └─utils                      # 实用程序和第三方包的目录
│  └─routes                        # 路由分组
│      └─v1                        # v1版本的api
│              user.py
│
└─test                             # 测试目录
        test_user.py
        __init__.py


```
