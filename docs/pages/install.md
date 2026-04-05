---
layout: default
title: Installation
---

# Installation

## Select your OS

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
<p><strong>Requirements:</strong><br>- Python 3 installed</p>
<p><strong>Install:</strong></p>
<pre><code>git clone https://github.com/Create-Lua/pyllia.git
cd pyllia\\sys
python Terminal.py</code></pre>
`,
    macos: `
<h3>macOS Installation</h3>
<p><strong>Requirements:</strong><br>- Python 3 installed</p>
<p><strong>Install:</strong></p>
<pre><code>git clone https://github.com/Create-Lua/pyllia.git
cd pyllia/sys
python3 Terminal.py</code></pre>
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
