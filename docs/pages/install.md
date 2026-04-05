---
layout: default
title: Installation
---

# Installation

Welcome to the Pyllia installation guide! Please select your operating system below to see the detailed installation instructions.

## Select Your OS

<select id="os-select">
  <option value="">--Choose OS--</option>
  <option value="windows">Windows</option>
  <option value="macos">macOS</option>
</select>

<div id="instructions" style="margin-top:20px;"></div>

<script>
const instructions = {
  windows: `
<h3>Windows Installation</h3>

<p><strong>Requirements:</strong></p>
<ul>
  <li>Windows 10 or higher</li>
  <li>Python 3.10+ installed (download from <a href="https://www.python.org/downloads/windows/">python.org</a>)</li>
  <li>Git installed (optional but recommended, <a href="https://git-scm.com/download/win">download here</a>)</li>
</ul>

<p><strong>Step 1: Clone the Repository</strong></p>
<pre><code>git clone https://github.com/Create-Lua/pyllia.git
cd pyllia\\sys</code></pre>

<p><strong>Step 2: Run Pyllia</strong></p>
<pre><code>python Terminal.py</code></pre>

<p><strong>Step 3: Optional Setup</strong></p>
<ul>
  <li>If you want Pyllia to be available globally, add Python to your PATH and create a shortcut to Terminal.py.</li>
  <li>You can also install community commands via the <code>fetch</code> command after running Pyllia.</li>
</ul>

<p><strong>Step 4: Verify Installation</strong></p>
<ul>
  <li>Run <code>help</code> inside Pyllia to see available commands.</li>
  <li>Try <code>hello</code> to test if the terminal is working properly.</li>
</ul>
`,

  macos: `
<h3>macOS Installation</h3>

<p><strong>Requirements:</strong></p>
<ul>
  <li>macOS 10.15 (Catalina) or higher</li>
  <li>Python 3.10+ installed (via <a href="https://www.python.org/downloads/mac-osx/">python.org</a> or Homebrew)</li>
  <li>Homebrew installed (optional but recommended, <a href="https://brew.sh/">brew.sh</a>)</li>
</ul>

<p><strong>Step 1: Install Git (if not installed)</strong></p>
<pre><code>brew install git</code></pre>

<p><strong>Step 2: Clone the Repository</strong></p>
<pre><code>git clone https://github.com/Create-Lua/pyllia.git
cd pyllia/sys</code></pre>

<p><strong>Step 3: Run Pyllia</strong></p>
<pre><code>python3 Terminal.py</code></pre>

<p><strong>Step 4: Optional Setup</strong></p>
<ul>
  <li>You can create an alias in your shell (e.g., Bash or Zsh) to run Pyllia easily from any directory:</li>
</ul>
<pre><code>echo "alias pyllia='python3 /path/to/pyllia/sys/Terminal.py'" >> ~/.zshrc
source ~/.zshrc</code></pre>

<ul>
  <li>Install community commands via the <code>fetch</code> command inside Pyllia.</li>
  <li>Verify installation by running <code>help</code> and <code>hello</code> inside Pyllia.</li>
</ul>
`
};

const select = document.getElementById('os-select');
const container = document.getElementById('instructions');

select.addEventListener('change', () => {
  const val = select.value;
  if(val && instructions[val]) {
    container.innerHTML = instructions[val];
  } else {
    container.innerHTML = '';
  }
});
</script>
