---
layout: default
title: Installation
---

# Installation

## Select your OS

<select id="os-select">
  <option value="">--Choose OS--</option>
  <option value="macos">macOS</option>
  <option value="windows">Windows</option>
</select>

<div id="instructions" style="margin-top:20px;"></div>

<script>
  const instructions = {
    macos: `
### macOS Installation

**Requirements:**
- Python 3 installed

**Install:**
\`\`\`bash
git clone https://github.com/Create-Lua/pyllia.git
cd pyllia/sys
python3 Terminal.py
\`\`\`
`,
    windows: `
### Windows Installation

**Requirements:**
- Python 3 installed

**Install:**
\`\`\`bash
git clone https://github.com/Create-Lua/pyllia.git
cd pyllia\\sys
python Terminal.py
\`\`\`
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
