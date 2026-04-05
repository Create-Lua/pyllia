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
  <li>Python 3.10+ installed (<a href="https://www.python.org/downloads/windows/">download here</a>)</li>
  <li>Optional: Git if you want, but not required</li>
</ul>

<p><strong>Step 1: Download Pyllia</strong></p>
<p>Go to the <a href="https://github.com/Create-Lua/pyllia/releases">Pyllia releases page</a> and download the latest <code>pyllia-zip.zip</code> file.</p>

<p><strong>Step 2: Extract the ZIP</strong></p>
<ul>
  <li>Right-click the downloaded zip and choose "Extract All..."</li>
  <li>Extract it to a folder you want to keep Pyllia in, e.g., <code>C:\Pyllia</code></li>
</ul>

<p><strong>Step 3: Run Pyllia</strong></p>
<pre><code>cd C:\\Pyllia\\sys
python Terminal.py</code></pre>

<p><strong>Step 4: Optional Setup</strong></p>
<ul>
  <li>You can create a shortcut to <code>Terminal.py</code> for easier access.</li>
  <li>Install community commands via the <code>fetch</code> command inside Pyllia.</li>
</ul>

<p><strong>Step 5: Verify Installation</strong></p>
<ul>
  <li>Run <code>help</code> inside Pyllia to see available commands.</li>
  <li>Try <code>hello</code> to test that the terminal works.</li>
</ul>
`,

  macos: `
<h3>macOS Installation</h3>

<p><strong>Requirements:</strong></p>
<ul>
  <li>macOS 10.15 (Catalina) or higher</li>
  <li>Python 3.10+ installed (<a href="https://www.python.org/downloads/mac-osx/">download here</a> or via Homebrew)</li>
  <li>Optional: Homebrew (<a href="https://brew.sh/">brew.sh</a>)</li>
</ul>

<p><strong>Step 1: Download Pyllia</strong></p>
<p>Go to the <a href="https://github.com/Create-Lua/pyllia/releases">Pyllia releases page</a> and download the latest <code>pyllia-zip.zip</code> file.</p>

<p><strong>Step 2: Extract the ZIP</strong></p>
<ul>
  <li>Double-click the zip file to extract it.</li>
  <li>Move the extracted folder to a convenient location, e.g., <code>~/Applications/Pyllia</code>.</li>
</ul>

<p><strong>Step 3: Run Pyllia</strong></p>
<pre><code>cd ~/Applications/Pyllia/sys
python3 Terminal.py</code></pre>

<p><strong>Step 4: Optional Setup</strong></p>
<ul>
  <li>Create an alias in your shell for easy access:</li>
</ul>
<pre><code>echo "alias pyllia='python3 /path/to/Pyllia/sys/Terminal.py'" >> ~/.zshrc
source ~/.zshrc</code></pre>

<ul>
  <li>Install community commands via the <code>fetch</code> command inside Pyllia.</li>
  <li>Verify installation by running <code>help</code> and <code>hello</code>.</li>
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
