# 🎵 植物大战僵尸 - 背景音乐系统完整指南

## 📋 目录
1. [快速开始](#快速开始)
2. [音乐文件说明](#音乐文件说明)
3. [音乐下载指南](#音乐下载指南)
4. [使用方法](#使用方法)
5. [常见问题](#常见问题)
6. [技术说明](#技术说明)

---

## 快速开始

### ✅ 三步搞定

#### 1️⃣ 准备音乐文件
你需要准备 5 个音乐文件（支持 .mp3, .ogg, .wav 格式）：

| 文件名 | 用途 | 建议长度 | 风格 |
|--------|------|----------|------|
| `mainmenu.mp3` | 主菜单音乐 | 1-3分钟 | 轻松、欢快 |
| `grasswalk.mp3` | 白天关卡音乐 | 2-4分钟 | 明快、活泼 |
| `moongrains.mp3` | 夜晚关卡音乐 | 2-4分钟 | 神秘、悠扬 |
| `victory.mp3` | 胜利音乐 | 5-20秒 | 欢快胜利 |
| `lose.mp3` | 失败音乐 | 5-20秒 | 低沉失败 |

#### 2️⃣ 放置文件
将音乐文件放入此文件夹（`resources/music/`）：
```
resources/
  └── music/
      ├── mainmenu.mp3
      ├── grasswalk.mp3
      ├── moongrains.mp3
      ├── victory.mp3
      └── lose.mp3
```

#### 3️⃣ 测试运行
```bash
# 测试音乐系统
python test_music.py

# 启动游戏
python main.py
```

---

## 音乐文件说明

### 📁 文件清单

- [ ] **mainmenu** - 主菜单背景音乐（循环播放）
- [ ] **grasswalk** - 白天关卡背景音乐（循环播放）
- [ ] **moongrains** - 夜晚关卡背景音乐（循环播放）
- [ ] **victory** - 胜利界面音乐（播放一次）
- [ ] **lose** - 失败界面音乐（播放一次）

### 🎵 音质建议

- **格式**: MP3 或 OGG（推荐）
- **比特率**: 128-192 kbps
- **采样率**: 44.1 kHz
- **声道**: 立体声
- **文件大小**: 建议单个文件 < 10 MB

### ⚠️ 重要提示

- 如果没有音乐文件，游戏仍然可以正常运行，只是没有背景音乐
- 文件名必须匹配（不包括扩展名部分）
- 支持的格式：`.mp3`, `.ogg`, `.wav`, `.midi`

---

## 音乐下载指南

### 方法 1：免费音乐资源网站（推荐）

#### 推荐网站

1. **Freesound** (https://freesound.org/)
   - 注册免费账号
   - 搜索关键词：menu music, game music, victory, defeat
   - 下载 CC0 或 CC-BY 许可的音乐

2. **OpenGameArt** (https://opengameart.org/)
   - 搜索 "background music"
   - 选择适合的游戏音乐
   - 注意查看许可证

3. **Incompetech** (https://incompetech.com/)
   - Kevin MacLeod 的免费音乐库
   - 按心情/类型浏览
   - 下载 MP3 格式

4. **Purple Planet Music** (https://www.purple-planet.com/)
   - 免费背景音乐
   - 多种风格可选

#### 搜索关键词建议

- **mainmenu**: "casual game menu", "happy background", "menu music"
- **grasswalk**: "upbeat game", "cheerful background", "adventure"
- **moongrains**: "mysterious", "night theme", "ambient"
- **victory**: "victory fanfare", "win jingle", "success"
- **lose**: "game over", "defeat sound", "sad"

### 方法 2：YouTube 音频库

1. 访问 YouTube 音频库 (https://www.youtube.com/audiolibrary)
2. 选择 "免费音乐" 标签
3. 按类型筛选
4. 下载并转换为 MP3 格式

### 方法 3：AI 音乐生成器

免费的 AI 音乐生成工具：
- **Soundraw** (https://soundraw.io/)
- **Mubert** (https://mubert.com/)
- **AIVA** (https://www.aiva.ai/)

### 方法 4：自己创作

使用免费的音乐制作软件：
- **LMMS** (https://lmms.io/) - 免费的数字音频工作站
- **Audacity** (https://www.audacityteam.org/) - 免费的音频编辑器
- **GarageBand** (Mac) - 苹果自带的音乐制作软件

### 文件格式转换

如果下载的音乐不是 MP3 格式，可以使用：

**在线转换工具**
- https://cloudconvert.com/
- https://convertio.co/

**桌面软件**
- Audacity - 免费，支持多种格式
- FFmpeg - 命令行工具

**FFmpeg 转换命令**
```bash
# 转换为 MP3
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3

# 转换为 OGG
ffmpeg -i input.wav -codec:a libvorbis -qscale:a 4 output.ogg
```

### 📝 版权注意事项

⚠️ **重要提示**：
1. 不要使用有版权的商业音乐
2. 使用免费音乐时，请遵守其许可证要求
3. 如果音乐要求署名，请在项目中添加 CREDITS.md 文件
4. 仅供个人学习和非商业用途

---

## 使用方法

### 🎮 音乐播放逻辑

游戏会在以下场景自动播放音乐：

| 场景 | 音乐文件 | 循环播放 |
|------|----------|----------|
| 主菜单 | mainmenu | 是 |
| 白天关卡 | grasswalk | 是 |
| 夜晚关卡 | moongrains | 是 |
| 胜利界面 | victory | 否（播放一次）|
| 失败界面 | lose | 否（播放一次）|

### ⚙️ 音量调整

编辑 `source/constants.py` 文件：

```python
MUSIC_VOLUME = 0.5  # 背景音乐音量 (0.0 到 1.0)
SOUND_VOLUME = 0.7  # 音效音量 (0.0 到 1.0)
```

### 🔇 关闭背景音乐

将音量设置为 0：
```python
MUSIC_VOLUME = 0.0
```

---

## 常见问题

### Q: 游戏没有声音？
A: 检查以下几点：
1. 音乐文件是否在正确位置（`resources/music/`）
2. 文件名是否正确
3. 运行 `python test_music.py` 诊断
4. 检查系统音量设置
5. 查看控制台是否有错误信息

### Q: 必须使用这些文件名吗？
A: 是的，文件名必须匹配（不包括扩展名部分）。如需使用其他文件名，需要修改 `source/constants.py` 中的常量。

### Q: 可以使用其他音频格式吗？
A: 可以，支持 MP3, OGG, WAV, MIDI。推荐使用 MP3 或 OGG 格式，兼容性好且文件小。

### Q: 没有音乐文件可以玩游戏吗？
A: 可以！游戏会正常运行，只是没有背景音乐。

### Q: 音乐文件应该多大？
A: 建议单个文件不超过 10MB，使用 128-192 kbps 的比特率。

### Q: 如何测试音乐系统？
A: 运行测试脚本：
```bash
python test_music.py
```

### Q: 可以添加音效吗？
A: 可以。创建 `resources/sounds/` 文件夹，在代码中使用 `pg.mixer.Sound()` 播放音效。

---

## 技术说明

### 🔧 音乐管理器类

游戏使用 `MusicManager` 类管理背景音乐：

```python
# 在游戏状态中使用
from source import tool
from source import constants as c

class MyGameState(tool.State):
    def startup(self, current_time, persist):
        # 播放音乐
        tool.music_manager.play_music(c.MUSIC_MAIN_MENU)
```

### 📊 音乐管理器功能

- `play_music(music_name, loops=-1)` - 播放音乐
- `stop_music()` - 停止音乐
- `pause_music()` - 暂停音乐
- `unpause_music()` - 恢复音乐
- `set_volume(volume)` - 设置音量

### 🎯 音乐播放流程

```
游戏启动
    ↓
初始化 pygame.mixer
    ↓
扫描 resources/music/ 文件夹
    ↓
加载音乐文件路径到字典
    ↓
游戏状态启动时调用 play_music()
    ↓
检查是否需要切换音乐
    ↓
加载并播放音乐文件
```

### 🛡️ 错误处理

- 文件不存在：打印警告，游戏继续运行
- 加载失败：捕获异常，打印错误信息
- 音频系统失败：优雅降级，不影响游戏

### 📝 已修改的文件

1. **source/constants.py** - 添加音乐相关常量
2. **source/tool.py** - 添加音乐加载和管理类
3. **source/state/mainmenu.py** - 主菜单播放音乐
4. **source/state/level.py** - 关卡播放音乐
5. **source/state/screen.py** - 胜利/失败界面播放音乐

### 🚀 未来扩展建议

#### 短期扩展
- 添加音效系统（射击、爆炸等）
- 在游戏中添加音量调节界面
- 添加音乐淡入淡出效果

#### 长期扩展
- 支持音乐播放列表
- 随机播放多首音乐
- 为不同关卡添加更多音乐变化
- 添加音乐可视化效果

#### 添加音效示例

```python
# 在 tool.py 中添加
def load_sounds(directory):
    sounds = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ('.wav', '.ogg'):
            sounds[name] = pg.mixer.Sound(
                os.path.join(directory, filename)
            )
    return sounds

# 使用
shoot_sound = SOUNDS['shoot']
shoot_sound.play()
```

---

## 📞 获取帮助

### 遇到问题？

1. **运行测试脚本**
   ```bash
   python test_music.py
   ```

2. **查看示例代码**
   ```bash
   python example_music_usage.py
   ```

3. **检查控制台错误信息**
   - 查看游戏运行时的输出
   - 注意警告和错误提示

### 测试清单

- [ ] 音乐文件已放置在 `resources/music/` 文件夹
- [ ] 文件名正确（不包括扩展名）
- [ ] 文件格式正确（MP3/OGG/WAV）
- [ ] 运行 `python test_music.py` 测试通过
- [ ] 运行 `python main.py` 游戏正常播放音乐

---

## 🎉 总结

背景音乐系统已成功集成到游戏中！

### 主要特性
- ✅ 完整的音乐管理系统
- ✅ 自动音乐切换
- ✅ 音量控制
- ✅ 多格式支持
- ✅ 错误处理和优雅降级

### 下一步
1. 准备音乐文件（从免费音乐网站下载）
2. 放置到 `resources/music/` 文件夹
3. 运行测试脚本验证
4. 启动游戏享受音乐！

---

**实现日期**: 2026年2月8日  
**版本**: 1.0.0

🎮 祝你游戏愉快！🎵
