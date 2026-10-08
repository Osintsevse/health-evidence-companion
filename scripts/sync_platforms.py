"""Synchronize host manifests from the portable plugin identity; no host settings changed."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def expected(root=ROOT):
    m=json.loads((root/'plugin.json').read_text(encoding='utf8'))
    claude={k:m[k] for k in ['name','version','description','author','homepage','repository','license']}
    codex={**claude,'skills':'./skills/','extensions':m['extensions']}
    catalog={'name':'health-evidence-companion-community','owner':m['author'],'plugins':[{'name':m['name'],'source':'./','description':m['description']}]}
    return {'.claude-plugin/plugin.json':claude,'.codex-plugin/plugin.json':codex,'.claude-plugin/marketplace.json':catalog}

def sync(root=ROOT):
    for name,value in expected(root).items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2)+'\n',encoding='utf8',newline='\n')
    print('Synchronized Claude Code and Codex manifests and Claude marketplace')
if __name__=='__main__':sync()
