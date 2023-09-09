from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Static

from source import Batch
from source import Settings
from source import XHS


def example():
    """通过代码设置参数，适合二次开发"""
    # 测试链接
    error_demo = "https://www.xiaohongshu.com/explore/"
    image_demo = "https://www.xiaohongshu.com/explore/64d1b406000000000103ee8d"
    video_demo = "https://www.xiaohongshu.com/explore/64c05652000000000c0378e7"
    # 实例对象
    path = "./"  # 作品下载储存根路径，默认值：当前路径
    folder = "Download"  # 作品下载文件夹名称（自动创建），默认值：Download
    proxies = None  # 网络代理
    timeout = 5  # 网络请求超时限制，默认值：10
    chunk = 1024 * 1024  # 下载文件时，每次从服务器获取的数据块大小，单位字节
    xhs = XHS(
        path=path,
        folder=folder,
        proxies=proxies,
        timeout=timeout,
        chunk=chunk, )  # 使用自定义参数
    # xhs = XHS()  # 使用默认参数
    download = True  # 是否下载作品文件
    # 返回作品详细信息，包括下载地址
    print(xhs.extract(error_demo))  # 获取数据失败时返回空字典
    print(xhs.extract(image_demo, download=download))
    print(xhs.extract(video_demo, download=download))


def main():
    """读取并应用配置文件设置的参数，适合一般作品文件下载需求"""
    xhs = XHS(**Settings().run())
    if ids := Batch().read_txt():
        for i in ids:
            xhs.extract(i.rstrip('\n'), download=True)
    else:
        while True:
            if url := input("请输入小红书作品链接："):
                xhs.extract(url, download=True)
            else:
                break


class RunMenu(Static):

    def compose(self) -> ComposeResult:
        yield Button("下载无水印图片/视频", id="run", variant="success")
        yield Button("读取文件并开始批量下载作品", id="batch", variant="success")
        yield Button("清空输入", id="reset", variant="error")


class XHSDownloader(App):
    CSS_PATH = "static/XHS_Downloader.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="结束运行"),
        Binding(
            key="w",
            action="repository",
            description="获取源码",
        ),
    ]

    def compose(self) -> ComposeResult:
        yield Label("请输入小红书图文/视频作品链接：")
        yield Input(placeholder="URL")
        yield RunMenu()
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "小红书作品采集工具"

    @staticmethod
    def action_repository():
        yield Label("Github Repository")


if __name__ == '__main__':
    # example()
    main()
    # app = XHSDownloader()
    # app.run()
