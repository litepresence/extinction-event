安装
=======================
**灭绝等级事件 - 集中交换必须死亡**

注意：此工具集目前处于alpha开发状态;即将推出更多新玩具！

(BTS) litpresence1 
----------------------


BitShares分散交换算法交易工具
--------------------------------


“灭绝事件”的名称源于这样一个概念：当分散交换技术和人工智能控制算法交易技术相结合并达到普通用户时：集中交换和月费算法交易将灭绝

收集硬件


这个堆栈在固态驱动器读/写时很重，需要4千兆字节的随机存取存储器，而中央处理速度相当于回测速度。

建议：

 - 任何尺寸的SSD固态驱动器; 120GB硬盘很不错。
 -  *请勿在旋转盘片硬盘上安装消光事件
 -  4 GB RAM满堆栈，8首选
 - 中高端桌面CPU，我使用的是AMD 7950
 - 金/白金电源


**安装 LINUX 操作系统**

任何debian / ubuntu都应该这样做。
堆栈不符合Mac或Windows标准。

我正在运行Cinnamon Mint 19.04，了解更多：

    https://linuxmint.com/

灭绝事件应该与其他Linux发行版兼容，安装可能会有所不同。


**更新 APT-GET**

    $ sudo apt-get update


**安装 PYTHON 3.6+**

我用过这些说明

    https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/

**SUDO APT-GET INSTALL 安装依赖项**

    $ sudo apt-get install -y python3-pip
    $ sudo apt-get install python3-tk
    $ sudo apt-get install python3-dev
    $ sudo apt-get install libsecp256k1-dev    
    $ sudo apt-get install git
    $ sudo pip3 install virtualenv

**克隆灭绝事件存储库**

从以下位置导航到您要运行机器人的文件夹：

    $ cd <文件夹名称>
    $ git clone https://github.com/litepresence/extinction-event.git

**创造虚拟环境**

输入灭绝事件文件夹：

    $ .../extinction-event
    $ virtualenv -p python3 env 

**进入虚拟环境**

    $ source env/bin/activate

**安装要求**

    $ pip install -r requirements.txt

*注意*虚拟环境和setup.py位于`extinction-event`
*注意*脚本全部在`extinction-event/EV`
*注意*您需要从灭绝事件文件夹激活您的虚拟环境每次运行这些脚本时都会启动新的终端选项卡。


**延误测试**

打开一个新的终端选项卡。运行延迟测试，需要几分钟时间。这将编写将由 metaNODE.py 使用的 nodes.txt 导航：

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 latencyTEST.py

当您更加认真地全面运行这些脚本时，可以在 latencyTEST.py 中更改 “USER CONTROLS” 以获得重复循环，自定义白名单，或扫描 github 以获取新发布的节点。您甚至可以绘制节点位置并将结果上传到互联网。在延迟测试编写了 node.txt 之后，在文本编辑器中打开 node.txt 以确认您有一个针对您所在区域的延迟排序节点列表。

**元节点**

接下来，您将开始第一个元节点会话。新的终端选项卡，cd导航到：

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 metaNODE.py


输入您的帐户名称和选择的市场。您可以按Enter跳过，将选择默认帐户和市场：

```
account: abc123
currency: open.btc
assest: bts
```


资本化对资产和货币无关紧要。 元节点 无法访问您的资金。

**微DEX**

这将确保您拥有所有依赖项来签署安装的事务。在新的终端选项卡中，metaNODE仍在第一个选项卡中运行，导航至：

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 microDEX.py

您将看到输入WIF的选项。或者，您可以按Enter键跳过。您无需在此时提供WIF以确保完整设置。

如果你给你的WIF，微DEX可以完全获得你的资金

在进入WIF之前，您应该让自己和朋友熟悉源代码。您的WIF是签署任何类型交易的标志。除非您理解并完全信任我提供给您的脚本，否则请勿进行身份验证。

获取WIF的最佳方法是打开参考Bitshares UI：

设置>>帐户>>显示键
点击钥匙图标
点击“以WIF格式显示私钥”

要获取参考UI的副本，请访问：

http://bitshares.org/download/


应用程序编程接口键

最新版本的测试引擎允许您对Bitshares DEX数据和几个外部源进行回测。我选择了这些来源中的每一个，因为有很多可用的数据，并且很容易获得免费密钥。

去获取钥匙：

    www.cryptocompare.com
    www.alphavantage.com
    www.nomics.com

打开apiKEYS.py并将密钥安装在字典中，保存文件并关闭

*注意*此py文件必须是json格式！
 - 除了最后一个条目后，在每个条目后使用双引号和逗号;没有逗号
 - 不包括本文档中的任何通知或其他文本

这些密钥是公共API密钥，如果被盗则无法影响您的资金，但它们会限制您的每日通话。他们需要保密;但不是像你的WIF那样的关键秘密。详情请见每个网站。

如果跳过此步骤，您将只能使用`tune_install（）`中的`CANDLE_SOURCE ='DEX'`进行回测，因为BitShares公共节点不需要密钥。

**数据集测试**

proxyTEST.py将确保您正确安装了密钥。

打开proxyTEST，脚本顶部附近有用户输入`API`。在`API`编号1到6上运行测试。

**灭绝等级事件**

在新的终端选项卡中，元节点仍在第一个选项卡中运行，导航至：

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 extinctionEVENT.py

您将看到一些选项：


** BACKTEST **允许您使用'extictionEVENT.py'中的`tune_install（）`来定义参数并调整策略盈利能力
** PAPER **允许您在不给机器人钱的情况下运行实时会话
    **LIVE** 是根据你的`control_panel（）`和`tune_install（）`设置进行实时交易
    **SALES** 允许您通过发布交易点图像而不显示移动平均阈值来销售消光EVV策略音乐
    **ORDER_TEST** 是一个带有基金的实时交易时段，但是会将订单放在远离边距的位置来测试身份验证

** OPTIMIZE **自动策略改进，目前尚未开源

**账户历史**

每当您的元节点正在运行时，您的帐户历史记录都会记录到文件中。 accountHISTORY.py可以读取此文件并绘制帐户余额随时间的变化。

**工具简介**


extinctionEVENT.py
------------
    移动平均交叉算法交易机器人框架交易Bitshares DEX
microDEX.py
------------
    轻量级用户界面，可在Bitshares DEX上执行手动购买/出售/取消操作
metaNODE.py
------------
    将来自多个公共DEX节点的市场数据统计为流式文本文件
latencyTEST.py
------------
    搜索您所在地区的低延迟Bitshares节点
proxyDEX.py
------------
    正确插补HLO​​CV Bitshares DEX蜡烛，用于回测和现场会话
proxyCEX.py
------------
    HLOCV altcoin：altcoin每日蜡烛，用于从cryptocompare.com进行回测
proxyMIX.py
------------
HLOCV从nomics.com交换特定的每日蜡烛以进行回测
proxyALPHA.py
------------
    HLOCV股票，外汇和加密：外汇日常蜡烛，用于从alphavantage.com进行回溯测试
apiKEYS.py
------------
    用于存储cryptocompare，alphavantage和nomics api密钥的字典
proxyTEST.py
------------
    用于从proxyDEX，CEX，MIX和ALPHA收集和绘制数据的实用程序
accountHISTORY.py
------------
    metaNODE.py 每当运行时每小时捕获一次余额，使用 accountHISTORY 进行可视化
访问litepresence.com获取机器优化算法
========================================================

你想让我调整你的算法吗？
我使用了成千上万的反向传播测试来使用精英量子粒子优化算法。
您可以尝试自己的优化算法，但为什么不让我的AI处理呢？

litepresence.com
