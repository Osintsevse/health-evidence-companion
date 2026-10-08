"""Build separate Claude upload ZIPs from the reviewed runtime allowlist."""
import io,json,shutil,zipfile,hashlib
from pathlib import Path
from validate import plugin_files
from sync_references import MAP

def build_platforms(root,dest):
    allowed=plugin_files(root);bundle=dest/'health-evidence-companion-claude-skills.zip'
    with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for skill in sorted(MAP):
            buffer=io.BytesIO()
            with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as single:
                prefix='skills/'+skill+'/'
                for rel in sorted(allowed):
                    if not rel.as_posix().startswith(prefix):continue
                    name=skill+'/'+rel.as_posix()[len(prefix):];item=zipfile.ZipInfo(name,(2026,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16;single.writestr(item,(root/rel).read_bytes())
            item=zipfile.ZipInfo(skill+'.zip',(2026,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16;z.writestr(item,buffer.getvalue())
    guide=dest/'PLATFORMS.md';shutil.copyfile(root/'docs/platforms.md',guide)
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [bundle,guide]}
