import fs from "fs";

function readJSON(path) {
  return fs.existsSync(path) ? JSON.parse(fs.readFileSync(path)) : [];
}

const docker = readJSON("docs/docker.json");

let md = `# m3tal-stack\n\n`;

md += `> **Role**: Infrastructure / Orchestration Layer\n`;
md += `> **Technology**: Docker Compose / Traefik\n\n`;

md += `## Overview\n`;
md += `This repository contains the standardized Docker Compose infrastructure for the M3TAL platform. It enforces path consistency, shared networking, and secure reverse proxying.\n\n`;

if (docker.length) {
  md += `## 🐳 Service Inventory\n`;
  // Group by stack
  const stacks = {};
  docker.forEach(s => {
    if (!stacks[s.stack]) stacks[s.stack] = [];
    stacks[s.stack].push(s);
  });

  Object.entries(stacks).forEach(([stackName, svcList]) => {
    md += `### ${stackName.charAt(0).toUpperCase() + stackName.slice(1)} Stack\n`;
    svcList.forEach(s => {
      md += `- **${s.name}** (${s.image})\n`;
      if (s.ports.length) {
        md += `  - Ports: ${s.ports.join(", ")}\n`;
      }
    });
    md += `\n`;
  });
}

md += `\n## M3TAL Ecosystem\n`;
md += `This is a sub-component of the [M3TAL Media Server](https://github.com/jakej985-rgb/M3tal-Media-Server).\n`;

fs.writeFileSync("README.generated.md", md);
console.log("README.generated.md assembled for M3TAL Stack.");
