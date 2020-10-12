# Excrement 💩 [![GitHub release](https://img.shields.io/github/v/tag/roudique/excrement)](https://github.com/roudique/excrement/releases)
A script to easily increment your Xcode project version.

#### Disclaimer:
Don't mind the code :) It's not of a very good quality, I have a limited knowledge of Python and just wrote this for fun and personal use.

## ❗️Pre-requisites:
- **Python 3**;<br>
- *(Optional)* **git**;
 
 ## 👉 Usage:
`excrement` is supposed to be used within the same folder where you have your `*.xcodeproj` file since it depends on parsing `project.pbxproj`.
 
 ---
 **See what the current version** in *.pbxproj is:<br>
 `excrement current`<br>

**Output:**<br>
```
Project version: 1.0
Build: 2
```

---
**Increment project version**:<br>
`excrement (major | minor | patch)`<br>

Currently `excrement` only works with project versions that have following format:<br>
`<MAJOR>.<MINOR>.<PATCH>` e.g. `1.0.3`.

⚠️ Running `major | minor | patch` will also increment your build number.

---
**Commit the increment in git**:<br>
`excrement (major | minor | patch) git`<br>

Adding `git` parameter will stage all files and commit them with message of the following format:<br>
`Upgrade to version <PROJECT_VERSION>, build <BUILD_NUMBER>`

---
**Add git tag**:<br>
`excrement (major | minor | patch) git tag`

This will also add git tag which equals to `<PROJECT_VERSION>` to the git commit.

## 🔧 Installation

To install, simply download `excrement.py` and run following commands in terminal:
1. `cp excrement.py excrement`
2. `chmod a+x excrement`
3. `mv excrement /usr/local/bin`

Done! Enjoy.

For any questions you can contact me at roudique@gmail.com
