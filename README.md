# LA 主页

+ [安装 zola](https://www.getzola.org/documentation/getting-started/installation/)
+ 查看网页
  > zola serve

## 添加论文

+ 进入 `utils/publications/all.bib` 文件夹，添加论文信息到 `all.bib` 文件中
+ 执行 `python3 utils/publications/update.py`，自动生成论文信息
+ 进入 `content/publications` 文件夹，修改论文相关信息
+ (*xzluo update*) 我的做法是在`test`文件夹执行上述操作，这样只会生成的新添加的论文，不会修改老的论文（`python3 utils/publications/update.py`已经修改为`test`路径）。然后将生成的publication剪切到`content/publications`文件夹，进一步修改。再将bibtex剪切到`static/bibtex`。
+ 

## 添加新闻

+ 在`utils/news/scir_news.xlsx`添加新闻信息，并在同一目录下另存为同名csv文件
+ 安装依赖 `pip3 install requests beautifulsoup4 lxml pyyaml`
+ 在项目根目录执行 `python3 utils/news/generate_news.py`，自动生成新闻信息。默认仅生成新添加的新闻，若要生成所有新闻，执行 `python3 utils/news/generate_news.py --overwrite`
+ 如新闻图片生成有误，可手动修改`content/news`中新闻文件的`image`项