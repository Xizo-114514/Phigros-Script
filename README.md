<div align="center">
<p align="center">
    <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/120782087/259819730-ac00f111-e9be-4824-81f8-3ebb6d6ba1f6.png" alt="phisap">
</p>

# Phigros-Script

✨ 一个可以自动循环打歌的Phigros脚本 ✨

轻松获取超多Data~

修改自[kvarenzn/phisap](https://github.com/kvarenzn/phisap)

</div>

## 目录
* [免责声明](#免责声明)
* [简介](#简介)
* [效果展示](#效果展示)
* [如何使用](#如何使用)
  * [准备](#准备)
  * [运行](#运行)
* [注意事项](#注意事项)
* [致谢](#致谢)
* [开源许可](#开源许可)

## 免责声明
+ 本项目属于个人兴趣项目，与厦门鸽游网络有限公司无关。
+ **本项目内不含任何版权素材，且本项目并非商业项目**。
+ 截止目前，项目作者从未在任何除GitHub以外的平台上以任何方式宣传过本项目。

## 简介

如你所见，这是一个用来刷Data的脚本，只要点按钮，就可以一直循环打歌，简单的获取大量Data。

+ 由于之前换手机，当时没出云存档功能，也忘了备份存档，所以旧的存档彻底没了。后来一段时间没玩Phi。
+ 而再次解锁精选集歌曲所需的Data实在不是小数目，于是就来找脚本了，没找到能用的，就在Phisap的基础上进行了修改。

  + 此处感谢一下，Phisap项目：[kvarenzn/phisap](https://github.com/kvarenzn/phisap)


---


![image](https://github.com/Xizo-114514/Phigros-Script/assets/120782087/7a94f162-bfbf-4d3f-8c86-7a3f3e9c1329)
B站UP总结的打Data最快的曲，链接：[论 Phigros 刷 Data 的最快方式](https://www.bilibili.com/read/cv15590536)

+ 目前Phigros有88首精选集，全部解锁需要87首16MB和1首打折4MB，总共1396MB。
  + 如果打BetterGraphicAnimation，需要把这个曲AP约1396次，最快也需要42.6小时。

所以写了这个程序，仅需要电脑后台挂着就能刷Data。
+ 选用了BetterGraphicAnimation和Engine x Start!!两个曲子
  + 一首是IN难度曲子中最快的，一首是更容易解锁的，没有适配更多，因为延迟不好调。

## 效果展示

![image](https://github.com/Xizo-114514/Phigros-Script/assets/120782087/4efe0cd8-8d69-4cbb-ae89-9f97fcd1e9fe)

打BetterGraphicAnimation速度大约11.67KB/s ，已经最快了

## 如何使用

### 准备

+ 1.首先你要先去配置好Phisap，链接：[kvarenzn/phisap](https://github.com/kvarenzn/phisap)
  + 在你已经顺利地使用Phisap完成一次自动打歌之后，你才可以使用本项目的程序。

+ 2.确认Phisap可以正常工作，然后下载本项目。

+ 3.直接把main_xizo.py放到Phisap目录中。与main.py同一目录即可。
  + 说明：我的main_xizo.py是由Phisap中的main.py修改与精简而来的，必须放在目录中运行。

### 运行

```bash
cd phisap # 将当前工作目录设置为phisap的根目录，或者直接在目录中右键选择“在终端中打开”（Win11）
python main_xizo.py
```
  + 程序内有提示，照做就可

## 注意事项

我的版本： Phigros 3.1.1.1 、 Python 3.11.4 、 Windows 11 、 BlueStacks 5.12.110.1006 P64模拟器 分辨率 960 x 536

+ 1.可能延迟对不上？可以尝试用同一个版本的Phigros。或者那就自己改改代码吧，就是245/249/251行的那几个值。

+ 2.程序跑不起来？用同版本Python试试。或者自己Debug。

+ 3.请只连接一个设备，可重置adb再次连接。

+ 4.建议用模拟器，连接手机比较麻烦，直接模拟器和脚本挂后台更方便。因为模拟器端口可能频繁变化，所以做了快速连接。

+ 5.模拟器建议降低分辨率，我用的960 x 536，更稳定点。如果出现异常问题，可以试试改分辨率。

+ 6.不要用WSA！之前用其他scrcpy脚本，怎么弄都不行，WSA有问题不要用，想找支持Hyper-V的模拟器可以用蓝叠64位，打不开就管理员运行。（亲身试出来的）

+ 7.别的自己研究研究不行再说。

## 致谢

[kvarenzn/phisap](https://github.com/kvarenzn/phisap)

[Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)

[Perfare/AssetStudio](https://github.com/Perfare/AssetStudio)

感谢上述优秀的项目和创造或维护它们的个人或企业。

## 开源许可

以WTFPL协议开源

好怪的协议名字......
