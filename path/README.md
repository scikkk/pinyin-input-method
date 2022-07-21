<!--
 * @Author: scikkk 203536673@qq.com
 * @Date: 2022-07-08 16:13:14
 * @LastEditors: scikkk
 * @LastEditTime: 2022-07-21 11:44:50
 * @Description: path config
-->
`python`解释器找不到自建模块，最后解决方法是：

将`path\mypinyin.pth`文件放入目录`D:\Users\86176\anaconda3\Lib\site-packages`，文件内容是

```
D:\_WangKe\0\mypinyin\src
```

即将项目路径加入运行环境，使解释器能够找到自建模块。