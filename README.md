![builddoc-banner](./docs/assets/builddoc-bg.png)
<p align="center">
	<a href="https://github.com/itsamedood/BuildDoc/blob/main/LICENSE">
		<img src="https://img.shields.io/github/license/itsamedood/BuildDoc?color=blue&style=for-the-badge">
	</a>
	<a href="https://lgtm.com/projects/g/itsamedood/BuildDoc/?mode=list">
		<img src="https://img.shields.io/lgtm/grade/python/github/itsamedood/BuildDoc?style=for-the-badge">
	</a>
	<a href="https://github.com/itsamedood/BuildDoc">
		<img src="https://img.shields.io/github/stars/itsamedood/BuildDoc?style=for-the-badge">
	</a>
</p>

# **BuildDoc Repository**
- ### [Documentation](./docs/00-Welcome.md)
- ### [Basic Installation](#basic-installation)

# Installation
> ## Basic Installation
> ### Steps
> Go to [releases](https://github.com/itsamedood/BuildDoc/releases/), download the version for your OS.
> To use in shells (linux/mac), add the following to `.bashrc` or `.zshrc`, etc, depending on which shell you're using:
>
> `alias build="/path/to/builddoc-bin"`
>
> Then run `build` whenever you want to run BuildDoc.
>
> For example, if you install BuildDoc to your desktop folder, you would do:
> 
> ### MACOS
> `alias build="$HOME/Desktop/BuildDoc/bin/macos/builddoc-bin"`
> ---
> ### LINUX
> `alias build="~/Desktop/BuildDoc/bin/macos/builddoc-bin"`
> ---
> ### WINDOWS
> I haven't gotten it working on Windows yet, sorry!
> ---

> ## Installing from source (advanced) (I haven't tested this 🙂)
> ### Steps
> Install python somehow.
> 
> Clone this project's source code by either downloading the zip, or with `git clone https://github.com/itsamedood/BuildDoc`.
> 
> Set an alias in your shell config file, like mentioned earlier, but `alias build="python /path/to/builddoc/src/main.py"`.
> ---
You do not *need* to use an alias for the shell commands, you can just run whatever is in the quotes("") instead, it's just slower for you.
---
